# Imported libraries 
import pandas as pd
import re
from dateutil import parser

"""
Standardize datetime columns to consistent date format

To standardize datetime columns with DateTime_Standardization.py, there are three important parameters. 
One is column which specifies which column to standardize. The second is american which determines 
the date format interpretation. The third is handle_invalid which controls how invalid dates are handled.

Column Selection (column):
    - Required: Must specify which column in the dataset contains dates

Date Format (american):
    - False: European format DD/MM/YYYY, DD/MM/YY (default)
    - True: American format MM/DD/YYYY, MM/DD/YY
    - Unambiguous of parameter american: Year-first formats, always the format YYYY/MM/DD
    - Unambiguous of parameter american: Text-month formats (e.g. Jan 2, 2025 or 15 January 2024)
    - Unambiguous of parameter american: Year-middle formats (../YYYY/...), directly invalid handling

Invalid Date Handling (handle_invalid):
    - 'nat': Set invalid dates to NaT (default)
    - 'delete': Delete entire row containing invalid date

Convention two-digit-year (dateutil):
    - 00-69 -> 2000-2069
    - 69 - 99 -> 1969-1999 

Logic of parsing text-month formats (dateutil):
    1. Extract month (text)
    2. Two numbers remain, one is day and one is year:
       if one is 4 digit -> year
       elif one is > 31 -> year 
       else (only two digits, both below 31):
          positon decides, closer to month or at beginning -> day 

Validation Rules (applied to all formats):
    - Month must be between 1 and 12
    - Day must be valid for that month (e.g., max 31 for January, max 30 for April)
    - Leap years are handled correctly (Feb 29 valid only in leap years)
    - Year must be between 1500 and 2100
    - If any rule fails → date is invalid → handle_invalid is applied

Invalid Detection Examples:
    - European mode (american=False): 
      01/25/2024 is invalid (month = 25 > 12)
      31/04/2024 is invalid (April only has 30 days)
    - American mode (american=True): 
      25/01/2024 is invalid (month = 25 > 12)
      02/29/2023 is invalid (2023 is not a leap year)
    - Year-first formats:
      2024/15/01 is invalid (month = 15 > 12)
    - Text-month formats:
      Feb 30, 2024 is invalid (February does not have 30 days)

Returns: 
    Cleaned dataframe and report (as tuple)
"""

# =============================================================================
# Main Function (Public)
# =============================================================================

def standardize_datetime(df: pd.DataFrame, 
                         column: str, 
                         american: bool = False,
                         handle_invalid: str = 'nat') -> tuple:
    # Work with copy, to not modify input df 
    df_work = df.copy()
    
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
        'invalid_detail': []
    }
    
    # Validate column parameter
    if column not in df_work.columns:
        print(f"Standardizing datetime... ERROR: Column '{column}' not found")
        return df_work, report
    
    # Validate handle_invalid parameter
    valid_options = ['nat', 'delete']
    if handle_invalid not in valid_options:
        print(f"Standardizing datetime... ERROR: Invalid option '{handle_invalid}'")
        return df_work, report
    
    # Set dayfirst based on american parameter
    dayfirst = not american
    # Note: dayfirst=True means European (DD/MM), dayfirst=False means American (MM/DD)
    
    format_name = "American (MM/DD)" if american else "European (DD/MM)"
    report['format'] = format_name
    
    # Track results
    report['total'] = len(df_work[column])
    report['missing_before'] = int(df_work[column].isna().sum())
    
    i_rows_to_delete = []
    # Note: i_ prefix indicates internal variable (list of row indices to delete)
    
    # Terminal output: start
    print("Standardizing datetime... ", end="", flush=True)
    
    # Process each row
    for idx in df_work.index:
        value = df_work.at[idx, column]
        # Note: .at[idx, column] gets single value at row idx, column name
        
        # Handle empty values
        if pd.isna(value) or value == '' or value is None:
            df_work.at[idx, column] = pd.NaT
            # Note: pd.NaT is pandas "Not a Time" - equivalent of NaN for datetime
            continue
        
        value_str = str(value).strip()
        if not value_str:
            df_work.at[idx, column] = pd.NaT
            continue
        
        # Parse and validate the date
        parsed_result, is_valid = _parse_and_validate(value_str, dayfirst)
        
        if is_valid:
            # Date is valid for chosen format
            df_work.at[idx, column] = parsed_result
            report['converted'] += 1
        
        else:
            # Date is invalid - handle according to handle_invalid parameter
            report['invalid'] += 1
            
            if handle_invalid == 'nat':
                df_work.at[idx, column] = pd.NaT
                report['issues'].append({
                    'row': idx,
                    'original': value_str,
                    'action': 'set to NaT',
                    'result': 'NaT'
                })
            
            elif handle_invalid == 'delete':
                i_rows_to_delete.append(idx)
                report['issues'].append({
                    'row': idx,
                    'original': value_str,
                    'action': 'row deleted',
                    'result': 'NaT'
                })
    
    # Delete rows if needed
    if i_rows_to_delete:
        df_work = df_work.drop(i_rows_to_delete).reset_index(drop=True)
        # Note: .drop() removes rows by index
        #       .reset_index(drop=True) resets index to 0,1,2,... and doesn't keep old index as column
        report['rows_deleted'] = i_rows_to_delete
    
    # Terminal output: end
    print("✓")
    
    return df_work, report

# =============================================================================
# Helper Functions (Private)
# =============================================================================

def _parse_and_validate(value_str: str, dayfirst: bool) -> tuple:
    """
    Parse date string and validate against chosen format and year range.
    
    Returns:
        (parsed_result, is_valid)
        - parsed_result: Correctly parsed datetime or NaT
        - is_valid: True if date is valid for chosen format AND year in range
    """
    try:
        # Check for year in middle (always invalid - no standard uses this format)
        if _is_year_in_middle(value_str):
            return pd.NaT, False
        
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
            yearfirst = False
            use_dayfirst = dayfirst
        
        # Check if date would need autocorrect (= invalid for chosen format)
        if _would_need_autocorrect(value_str, dayfirst):
            return pd.NaT, False
        
        # Parse the date with dateutil
        parsed = parser.parse(value_str, dayfirst=use_dayfirst, yearfirst=yearfirst)
        
        # Validate year range (1500-2100)
        if parsed.year < 1500 or parsed.year > 2100:
            return pd.NaT, False
        
        return parsed.date(), True
    
    except (ValueError, TypeError, parser.ParserError):
        # Could not parse at all
        return pd.NaT, False

def _is_year_in_middle(value_str: str) -> bool:
    """
    Check if 4-digit year is in middle position.
    Format like "01/2024/15" is always invalid - no standard uses this.
    
    Returns:
        True if year is in middle position (invalid format)
    """
    # Skip text-based dates (text month formats are handled differently)
    if any(c.isalpha() for c in value_str):
        return False
    
    # Extract parts
    parts = re.split(r'[/\-\.]', value_str)
    # Note: r'[/\-\.]' is regex pattern matching / or - or .
    
    if len(parts) != 3:
        return False
    
    # Check if middle part is 4-digit year
    middle = parts[1].strip()
    if len(middle) == 4 and middle.isdigit():
        year = int(middle)
        if 1500 <= year <= 2100:
            return True
    
    return False

def _would_need_autocorrect(value_str: str, dayfirst: bool) -> bool:
    """
    Check if dateutil would need to autocorrect (swap day/month).
    If autocorrect needed, the date is invalid for the chosen format.
    
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