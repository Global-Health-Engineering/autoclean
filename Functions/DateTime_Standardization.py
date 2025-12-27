# Imported libraries 
import pandas as pd
import re
from dateutil import parser

"""
Standardize datetime columns to pandas datetime64 format

To standardize datetime columns with DateTime_Standardization.py, there are three important parameters. 
One is column which specifies which column to standardize. The second is american which determines 
the date format interpretation. The third is handle_invalid which controls how invalid dates are handled.

Column Selection (column):
    - Required: Must specify which column in the dataset contains dates

Date Format (american):
    - False: European format DD/MM/YYYY, DD/MM/YY (default)
    - True: American format MM/DD/YYYY, MM/DD/YY 
    - Year-first and text-month formats are unambiguous and ignore this parameter

Invalid Date Handling (handle_invalid):
    - 'nat': Set invalid dates to NaT (default)
    - 'delete': Delete entire row containing invalid date
    - 'interactive': Ask user for each invalid date (options: NaT, delete row, Autocorrect by dateutil, manual entry)

Autocorrect by dateutil (available in interactive mode):
    - When a date is invalid for the chosen format, dateutil internally tries the opposite format.
    - Example: User selects European, input is "01/25/2024"
      European: Day=01, Month=25 → Invalid (25 > 12)
      Dateutil tries American: Month=01, Day=25 → January 25, 2024 → Valid
    - In interactive mode, user can choose to accept this autocorrected result.
    - If both formats fail (e.g., "31/04/2024"), autocorrect is not available → NaT or delete.

Validation Rules (applied to all formats):
    - Month must be between 1 and 12
    - Day must be valid for that month (e.g., max 31 for January, max 30 for April)
    - Leap years are handled correctly (Feb 29 valid only in leap years)
    - Year must be between 1500 and 2100
    - If any rule fails → date is invalid → handle_invalid is applied

Invalid Detection Examples:
    - European mode (american=False): 01/25/2024 is invalid (25 > 12, can't be month)
    - American mode (american=True): 25/01/2024 is invalid (25 > 12, can't be month)
    - Both modes: 31/04/2024 is invalid (April has only 30 days)
    - Both modes: 29/02/2023 is invalid (2023 is not a leap year)
"""


# =============================================================================
# Main Function (Public)
# =============================================================================

def standardize_datetime(df: pd.DataFrame, 
                         column: str, 
                         american: bool = False,
                         handle_invalid: str = 'nat') -> tuple:
    """
    Returns:
        (df, report): Cleaned DataFrame and report dict for cleaning report
    """
    
    df = df.copy()
    # Note: .copy() creates a copy of the dataframe to avoid modifying the original
    
    # Initialize report
    report = {
        'column': column,
        'format': None,
        'handle_invalid': handle_invalid,
        'total': 0,
        'missing_before': 0,
        'converted': 0,
        'invalid': 0,
        'rows_deleted': [],
        'issues': []
    }
    
    # Validate column parameter
    if column not in df.columns:
        print(f"Standardizing datetime... ERROR: Column '{column}' not found")
        return df, report
    
    # Validate handle_invalid parameter
    valid_options = ['nat', 'delete', 'interactive']
    if handle_invalid not in valid_options:
        print(f"Standardizing datetime... ERROR: Invalid option '{handle_invalid}'")
        return df, report
    
    # Set dayfirst based on american parameter
    dayfirst = not american
    # Note: dayfirst=True means European (DD/MM), dayfirst=False means American (MM/DD)
    
    format_name = "American (MM/DD)" if american else "European (DD/MM)"
    report['format'] = format_name
    
    # Track results
    report['total'] = len(df[column])
    report['missing_before'] = int(df[column].isna().sum())
    
    i_rows_to_delete = []
    # Note: i_ prefix indicates internal variable (list of row indices to delete)
    
    had_interactive = False
    # Track if we had interactive prompts (to reprint step name at end)
    
    # Terminal output: start
    print("Standardizing datetime... ", end="", flush=True)
    
    # Process each row
    for idx in df.index:
        value = df.at[idx, column]
        # Note: .at[idx, column] gets single value at row idx, column name
        
        # Handle empty values
        if pd.isna(value) or value == '' or value is None:
            df.at[idx, column] = pd.NaT
            # Note: pd.NaT is pandas "Not a Time" - equivalent of NaN for datetime
            continue
        
        value_str = str(value).strip()
        if not value_str:
            df.at[idx, column] = pd.NaT
            continue
        
        # Parse and validate the date
        parsed_result, is_valid, needs_autocorrect, autocorrect_result = _parse_and_validate(value_str, dayfirst)
        
        if is_valid:
            # Date is valid for chosen format
            df.at[idx, column] = parsed_result
            report['converted'] += 1
        
        else:
            # Date is invalid - handle according to handle_invalid parameter
            report['invalid'] += 1
            
            # If interactive, print newline before first prompt
            if handle_invalid == 'interactive' and not had_interactive:
                print()  # Newline after "Standardizing datetime... "
                had_interactive = True
            
            action, final_value = _handle_invalid_date(
                idx, value_str, autocorrect_result, american, 
                handle_invalid, i_rows_to_delete, needs_autocorrect
            )
            df.at[idx, column] = final_value
            
            # Add to report
            result_str = final_value.strftime('%Y-%m-%d') if pd.notna(final_value) else "NaT"
            report['issues'].append({
                'row': idx,
                'original': value_str,
                'action': action,
                'result': result_str
            })
    
    # Delete rows if needed
    if i_rows_to_delete:
        df = df.drop(i_rows_to_delete).reset_index(drop=True)
        # Note: .drop() removes rows by index
        #       .reset_index(drop=True) resets index to 0,1,2,... and doesn't keep old index as column
        report['rows_deleted'] = i_rows_to_delete
    
    # Terminal output: end
    if had_interactive:
        print("Standardizing datetime... ✓")  # Reprint with checkmark
    else:
        print("✓")  # Just checkmark on same line
    
    return df, report


# =============================================================================
# Helper Functions (Private)
# =============================================================================

def _parse_and_validate(value_str: str, dayfirst: bool) -> tuple:
    """
    Parse date string and validate against chosen format and year range.
    
    Returns:
        (parsed_result, is_valid, needs_autocorrect, autocorrect_result)
        - parsed_result: Correctly parsed datetime or NaT
        - is_valid: True if date is valid for chosen format AND year in range
        - needs_autocorrect: True if dateutil had to swap day/month
        - autocorrect_result: The auto-corrected datetime (if swap happened)
    """
    try:
        # Determine parsing settings based on format detection
        if _is_two_digit_format(value_str):
            # Two-digit year (01/02/03): year is always last
            yearfirst = False
            use_dayfirst = dayfirst
        elif _is_year_first(value_str):
            # Year-first (2024-12-01): always YYYY-MM-DD, ignore dayfirst
            yearfirst = True
            use_dayfirst = False
        else:
            # Year-last (15/01/2024): use dayfirst parameter
            yearfirst = True
            use_dayfirst = dayfirst
        
        # Check if dateutil would need to autocorrect (swap day/month)
        needs_autocorrect = _would_need_autocorrect(value_str, dayfirst)
        
        # Parse the date with dateutil
        parsed = parser.parse(value_str, dayfirst=use_dayfirst, yearfirst=yearfirst)
        
        # Validate year range (1500-2100)
        if parsed.year < 1500 or parsed.year > 2100:
            return pd.NaT, False, False, pd.NaT
        
        if needs_autocorrect:
            # Date was auto-corrected by dateutil
            # Return: invalid for chosen format, but autocorrect available
            return pd.NaT, False, True, parsed
        else:
            # Date is valid for chosen format
            return parsed, True, False, pd.NaT
    
    except (ValueError, TypeError, parser.ParserError):
        # Could not parse at all
        return pd.NaT, False, False, pd.NaT


def _would_need_autocorrect(value_str: str, dayfirst: bool) -> bool:
    """
    Check if dateutil would need to autocorrect (swap day/month).
    
    This happens when the format doesn't match:
    - European (dayfirst=True): expects DD/MM, but second value > 12
    - American (dayfirst=False): expects MM/DD, but first value > 12
    """
    # Skip text-based dates (always unambiguous - no autocorrect needed)
    if any(c.isalpha() for c in value_str):
        return False
    
    # Extract numeric parts
    parts = re.split(r'[/\-\.]', value_str)
    # Note: r'[/\-\.]' is regex pattern matching / or - or .
    #       The \ escapes - and . which have special meaning in regex
    
    numeric_parts = []
    for p in parts:
        p = p.strip()
        if p.isdigit():
            numeric_parts.append(int(p))
    
    if len(numeric_parts) < 2:
        return False
    
    first, second = numeric_parts[0], numeric_parts[1]
    
    # Skip year-first formats (always YYYY-MM-DD, no autocorrect)
    if len(parts) >= 1 and len(parts[0].strip()) == 4:
        return False
    
    if dayfirst:
        # European: expect day first (≤31), month second (≤12)
        # Autocorrect needed if: first ≤ 12 AND second > 12 (second can't be month)
        if first <= 12 and second > 12:
            return True
    else:
        # American: expect month first (≤12), day second (≤31)
        # Autocorrect needed if: first > 12 (first can't be month)
        if first > 12 and second <= 12:
            return True
    
    return False


def _handle_invalid_date(row_idx: int, 
                         original: str, 
                         autocorrect_result,
                         american: bool,
                         handle_invalid: str,
                         rows_to_delete: list,
                         autocorrect_available: bool) -> tuple:
    """
    Handle an invalid date based on handle_invalid setting.
    
    Returns:
        (action_taken, final_value)
    """
    if handle_invalid == 'nat':
        return "set to NaT", pd.NaT
    
    elif handle_invalid == 'delete':
        rows_to_delete.append(row_idx)
        return "row deleted", pd.NaT
    
    elif handle_invalid == 'interactive':
        return _interactive_prompt(row_idx, original, autocorrect_result, 
                                   american, rows_to_delete, autocorrect_available)
    
    return "unknown", pd.NaT


def _interactive_prompt(row_idx: int,
                        original: str,
                        autocorrect_result,
                        american: bool,
                        rows_to_delete: list,
                        autocorrect_available: bool) -> tuple:
    """
    Ask user how to handle invalid date.
    
    Returns:
        (action_taken, final_value)
    """
    current_format = "American (MM/DD)" if american else "European (DD/MM)"
    other_format = "European (DD/MM)" if american else "American (MM/DD)"
    
    print(f"\n  Row {row_idx}: \"{original}\" is invalid for {current_format} format.")
    print(f"    [1] Set to NaT (missing value)")
    print(f"    [2] Delete entire row")
    
    # Only show autocorrect option if available
    if autocorrect_available and pd.notna(autocorrect_result):
        autocorrect_str = autocorrect_result.strftime('%B %d, %Y')
        print(f"    [3] Autocorrect to {other_format} → {autocorrect_str}")
        print(f"    [4] Enter date manually")
        max_option = 4
    else:
        print(f"    [3] Enter date manually")
        max_option = 3
    
    while True:
        choice = input(f"    Your choice (1-{max_option}): ").strip()
        
        if choice == '1':
            return "set to NaT (user)", pd.NaT
        
        elif choice == '2':
            rows_to_delete.append(row_idx)
            return "row deleted (user)", pd.NaT
        
        elif choice == '3':
            if autocorrect_available and pd.notna(autocorrect_result):
                # Option 3 is autocorrect
                return f"autocorrect to {other_format} (user)", autocorrect_result
            else:
                # Option 3 is manual entry
                return _manual_entry()
        
        elif choice == '4' and max_option == 4:
            return _manual_entry()
        
        else:
            print(f"    Invalid choice. Enter 1-{max_option}.")


def _manual_entry() -> tuple:
    """
    Prompt user to enter date manually.
    
    Returns:
        (action_taken, final_value)
    """
    while True:
        manual_input = input("    Enter correct date: ").strip()
        try:
            manual_parsed = parser.parse(manual_input)
            # Validate year range
            if manual_parsed.year < 1500 or manual_parsed.year > 2100:
                print("    Year must be between 1500 and 2100. Try again.")
                continue
            return "manual entry (user)", manual_parsed
        except:
            print("    Could not parse date. Try again (e.g., '2024-01-15' or 'Jan 15, 2024').")


def _is_two_digit_format(value_str: str) -> bool:
    """
    Check if date string is two-digit format (e.g., 01/02/03).
    All three parts must be 1-2 digits.
    """
    parts = re.split(r'[/\-\.]', value_str)
    if len(parts) != 3:
        return False
    return all(len(p.strip()) <= 2 and p.strip().isdigit() for p in parts)


def _is_year_first(value_str: str) -> bool:
    """
    Check if date starts with 4-digit year (e.g., 2024-12-01).
    Year must be in range 1500-2100 to be detected as year-first.
    """
    parts = re.split(r'[/\-\.]', value_str)
    if len(parts) >= 1:
        first = parts[0].strip()
        if len(first) == 4 and first.isdigit():
            year = int(first)
            if 1500 <= year <= 2100:
                return True
    return False