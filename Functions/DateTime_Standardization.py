# Imported libraries 
import pandas as pd
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
    - Numeric dates need to consist out of 3 integer values (day, month & year), otherwise invalid (dateutil would add missing information)
    - Text-month formats need to have 2 numerical values (day & year), otherwise invalid (dateutil would add missing information)
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
    # Terminal output: start
    print("Standardizing datetime... ", end = "", flush = True)
    # Note: With flush = True, print is immediately
    
    # Work with copy, to not modify input df 
    df_work = df.copy()
    
    # Initialize report
    report = {
        'column': column,
        'format': None,
        'handle_invalid': handle_invalid,
        'total_values': 0,
        'n_standardized_dates': 0,
        'invalid': 0,
        'rows_deleted': 0,
        'details_invalid': []}
    
    # Validate column parameter
    if column not in list(df.columns):
        # Note: list(df.columns) gets list of column names
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    # Validate handle_invalid parameter
    valid_options = ['nat', 'delete']
    if handle_invalid not in valid_options:
        raise ValueError(f"Invalid option '{handle_invalid}'. Must be one of: {valid_options}")

    # Set dayfirst based on american parameter
    dayfirst = not american
    # Note: dayfirst = True means European (DD/MM), dayfirst = False means American (MM/DD)
    
    # Update report 
    report['format'] = "American (MM/DD)" if american else "European (DD/MM)"
    report['total_values'] = len(df_work[column])
    
    # Initialize list of indexes of rows to delete 
    i_rows_to_delete = []
    
    # Process each row resp. each value in the column with dates 
    for idx in list(df_work.index):
        # Note: list(df_work.index) gets list of row indexes 

        value = df_work.at[idx, column]
        # Note: .at[idx, column] gets the date to process 
        
        # Convert missing values to pd.NaT (type for missing date values )
        if pd.isna(value):
            # Note: pd.isna(value) is true if value is None, pd.NA, pd.NaT, np.nan
            df_work.at[idx, column] = pd.NaT
            continue
            # Note: With continue jump to next iteration of the for loop
        
        # Convert value to string and remove leading & trailing whitespaces (needed for parser.parse())
        value_str = str(value).strip()

        # Parse (= convert raw data into structured format) and validate the date
        parsed_result, is_valid = _parse_and_validate(value_str, dayfirst)
        # Note: If is_valid = true, all validation rules apply, if not is_valid = false (invalid date)

        if is_valid:
            # Standardize valid date and update report 
            df_work.at[idx, column] = parsed_result
            report['n_standardized_dates'] += 1
        
        else:
            # Handle invalid date according handle_invalid parameter

            # Update report 
            report['invalid'] += 1
            
            if handle_invalid == 'nat':
                df_work.at[idx, column] = pd.NaT

                # Update report 
                report['details_invalid'].append({'row': idx,
                                                 'original': value_str,
                                                 'action': 'set to NaT'})
            
            elif handle_invalid == 'delete':
                # Update indexes of rows to delete 
                i_rows_to_delete.append(idx)

                # Update report 
                report['details_invalid'].append({'row': idx,
                                                 'original': value_str,
                                                 'action': 'row deleted'})
    
    # Delete rows if needed (this needs to be outside for loop, otherwise rows would be skipped)
    if len(i_rows_to_delete) > 0:
        df_work = df_work.drop(i_rows_to_delete).reset_index(drop = True)
        # Note: .drop(list) removes all rows which indexes are in list 
        #       .reset_index(drop = True) resets row indexes

        # Update report 
        report['rows_deleted'] = len(i_rows_to_delete)
    
    # Terminal output: end
    print("✓")
    
    return df_work, report

# =============================================================================
# Helper Functions (Private)
# =============================================================================

def _parse_and_validate(value_str: str, dayfirst: bool) -> tuple:
    """
    Parse date string and check if validation rules apply

    Returns:
        parsed_result & is_valid (as tuple)
    
    Note: 
        - If is_valid = true (i.e. all validation rules apply) parsed_result = correctly parsed datetime, otherwise (is_valdi = false) parsed_result = pd.NaT
        - With try & except, all code in try: is run and if a parser.ParserError appears from parser.parse() code in except: is run
        - parser.ParserError appears if some of validation rules do not hold (e.g. parser.parse("Feb 30, 2024") -> Feb doesn't have 30 days) or when dateutil doesn't recognize any date pattern in the string (e.g. parser.parse("!!!???"))
        - Further our code validates: text-month format (needs 2 numerical values (day & year)), numeric dates (needs 3 integer values (day, month, year)) & year range (1500-2100), as this is not checked by dateutil or dateutil adds information if some is missing
        - Also dateutil applies autocorrection (swapping day/month, if month > 12 and day < 12), this is avoided by our code and date is then invalid 
    """

    try:
        is_text_month = _is_text_month_format(value_str)

        if is_text_month:
            if not _validate_text_month_format(value_str): 
                return pd.NaT, False
        else:
            if not _validate_numerical_date(value_str): 
                return pd.NaT, False
            
        # Check for year in middle -> invalid
        if _is_year_in_middle(value_str):
            return pd.NaT, False
        
        # Determine yearfirst parameter for parser.parse()
        if _is_year_first(value_str):
            # For year-first (YYYY/MM/DD), yearfirst = True
            yearfirst = True
        else:
            # For other formats, yearfirst = False 
            yearfirst = False
        
        # Parse the date with dateutil
        parsed = parser.parse(value_str, dayfirst = dayfirst, yearfirst = yearfirst)
        
        # Check if dateutil autocorrected (swapped day/month)
        if _was_autocorrected(value_str, parsed, dayfirst):
            return pd.NaT, False
        
        # Validate year range (1500-2100)
        if parsed.year < 1500 or parsed.year > 2100:
            return pd.NaT, False
        
        return parsed.date(), True
        # Note: parser.parse() returns a datetime object, which includes time -> return only date without time (parsed.date())

    except parser.ParserError:
        return pd.NaT, False
    
def _is_text_month_format (value_str: str) -> bool: 
    """
    Check if date (value_str) is text-month format (true, if date has at least one alphabetic character)
    
    Returns:
        True if date (value_str) is text-motnh, otherwise false    
    """
    has_text = False 
    for char in value_str:
            if char.isalpha():
                # Note: char.isalpha() = true if the character char is alphabetic (a-z, A-Z)
                has_text = True
                break # break exit the for loop 
    
    return has_text

def _validate_text_month_format (value_str: str) -> bool:
    """
    Check if text-month format date (value_str) is valid (needs 2 numerical values (day, year))

    Returns:
        True if text-month format date (value_str) is valid, otherwise false

    Note: Assuming here, value_str is text-month format   
    """

    # Count numerical values in text-month format
    numbers = [] # List to store numerical values
    current_num = "" # Used as temporary storage
    for char in value_str:
        # If character is digit store it in current_num
        if char.isdigit():
            current_num += char
        else:
            # If current_num is not empty and current character is not a digit, current_num stores a numerical value
            # Hence append it to numbers and reset current_num
            if len(current_num) > 0:
                numbers.append(current_num)
                current_num = ""

    # If a numerical value is at the end its still saved in current_num and not appended to numbers
    # Hence append it to numbers 
    if len(current_num) > 0:  
        numbers.append(current_num)
    
    if len(numbers) == 2: 
        return True
    
    return False
    
def _validate_numerical_date(value_str: str) -> bool:
    """
    Check if numeric date (value_str) is valid, i.e. has 3 integer values (day, month, year)

    Returns:
        True if numeric date is valid, otherwise false
    
    Note: Assuming here, value_str is numerical date
    """

    # Replace possible seperator of value_str with / and split value_str by / into list 
    parts = value_str.replace('-', '/').replace('.', '/').replace(' ', '/').replace(':', '/').split('/')
            
    # Remove possible leading/trailing whitespaces in elements of parts
    parts = [part.strip() for part in parts]

    # Parts must have exactly 3 values (day, month, year), otherwise invalid numeric date
    if len(parts) != 3:
        return False
            
    # All parts must be integers and cannot be empty strings, otherwise invalid numeric date
    for part in parts:
        if not part.isdigit():
            # Note str.isdigit() is true if str consists only of integers and is not empty, otherwise false  
            return False
    
    return True
        
def _was_autocorrected(value_str: str, parsed, dayfirst: bool) -> bool:
    """
    Check if dateutil autocorrected by comparing parsed result with input
    
    Returns:
        True if dateutil autocorrected, otherwise false
    """

    # Return false for text-month formats (no autocorrection there)
    if _is_text_month_format(value_str): 
        return False

    # Replace possible seperator of value_str with / and split value_str by / into list 
    parts = value_str.replace('-', '/').replace('.', '/').replace(' ', '/').replace(':', '/').split('/')
    
    # Remove possible leading/trailing whitespaces in elements of parts
    parts = [part.strip() for part in parts]

    # Return false for year-first formats (no autocorrection there)
    if len(parts[0]) == 4:
        return False
    
    # Convert first element of parts to integers
    first = int(parts[0])

    # Check if parsed was autocorrected by dateutil 
    if dayfirst:
        # European: expected first = day
        return parsed.day != first 
    else:
        # American: expected first = month
        return parsed.month != first 

def _is_year_in_middle(value_str: str) -> bool:
    """
    Check if nummeric date (value_str) has 4-digit year in middle position (e.g. 01/2024/15)
  
    Returns:
        True if year is in middle position, otherwise false

    Note: Assuming here, value_str is numerical date
    """

    # Return false for text-month formats 
    if _is_text_month_format(value_str): 
        return False
    
    # Replace possible seperator of value_str with / and split value_str by / into list 
    parts = value_str.replace('-', '/').replace('.', '/').replace(' ', '/').replace(':', '/').split('/')
    
    # Remove possible leading/trailing whitespaces in elements of parts
    parts = [part.strip() for part in parts]

    # Check if middle part is 4-digit year
    if len(parts[1]) == 4:
        return True
    
    return False

def _is_year_first(value_str: str) -> bool:
    """
    Check if numeric date (value_str) starts with 4-digit year (e.g. 2024-12-01)

    Returns:
        True if format is year-first (YYYY/MM/DD), otherwise false

    Note: Assuming here, value_str is numerical date
    """

    # Return false for text-month formats
    if _is_text_month_format(value_str): 
        return False
    
    # Replace possible seperator of value_str with / and split value_str by / into list 
    parts = value_str.replace('-', '/').replace('.', '/').replace(' ', '/').replace(':', '/').split('/')
    
    # Remove possible leading/trailing whitespaces in elements of parts
    parts = [part.strip() for part in parts] 

    # Check if first part is 4-digit year
    if len(parts[0]) == 4:
        return True
    
    return False