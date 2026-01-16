# Imported libraries
from datetime import datetime

"""
Generate cleaning report as markdown file

This function gets as an input a dictionary, consisting of every single report of each cleaning function, 
which was applied in the pipeline. Note each single report is again a dictionary. With this input a comprehensive 
report file (md file) is generated. 

Input (needs to have this structure):
    reports = {'preprocessing': report_pre,
               'duplicates': report_dup,
               'missing_values': report_miss,
               'datetime': report_date,          
               'outliers': report_out,
               'structural_errors': report_str,  
               'postprocessing': report_post}

Note: 
    - Only include reports for cleaning functions that were actually performed (missing keys will be skipped in the report)
    - Value of key 'structural_errors' can be a list of dictionaries, if Structural_Errors.py is applied multiple times

Principle of Markdown generation:
    1. Each line of the Markdown file is stored as a string in list 'lines'
    2. At the end, list 'lines' is converted into one long string with \n (newline character) between each element

Markdown syntax used:
    # Text          → Heading 1
    ## Text         → Heading 2
    ### Text        → Heading 3
    **Text**        → Bold
    - Item          → Bullet point
    ---             → Horizontal line
    | A | B |       → Table row
    |---|---|       → Table header separator (required after header row) 
"""

def generate_cleaning_report(reports: dict, filepath: str = 'cleaning_report.md', dataset_name: str = None) -> None:
    """
    Generate Markdown cleaning report from report dicts.
    
    Parameters:
        filepath: Output path for Markdown file (default = 'cleaning_report.md')
        dataset_name: Optional name of dataset for report (default = None)
    
    Returns:
        Function returns nothing (None), directly saves md file in desired location (filepath)
    """
    
    # Terminal output: start
    print("Generate cleaning report... ", end = "", flush = True)
    # Note: With flush = True, print is immediately

    # Initialize list of lines
    lines = []
    
    # Create Header
    lines.append("# AutoClean Report")
    lines.append("") # empty line 
    if dataset_name is not None:
        lines.append(f"**Dataset:** {dataset_name}")
    lines.append(f"**Generated:** {datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}") # Append line with current date & time
    lines.append("") # empty line
    
    # Create summary section
    lines.extend(_generate_summary(reports)) # Add returned list of _generate_summary() to lines
    # Note: list1.extend(list2) appends every element of list2 to list1  
    
    # Create preprocessing section (if key is not missing)
    if 'preprocessing' in reports:
        lines.extend(_generate_preprocessing_section(reports['preprocessing'])) # Add returned list of _generate_preprocessing_section() to lines
    
    # Create duplicates section (if key is not missing)
    if 'duplicates' in reports:
        lines.extend(_generate_duplicates_section(reports['duplicates'])) # Add returned list of _generate_duplicates_section() to lines
    
    # Create missing values section (if key is not missing)
    if 'missing_values' in reports:
        lines.extend(_generate_missing_values_section(reports['missing_values'])) # Add returned list of _generate_missing_values_section() to lines
    
    # Create datetime section (if key is not missing)
    if 'datetime' in reports:
        lines.extend(_generate_datetime_section(reports['datetime'])) # Add returned list of _generate_datetime_section() to lines
    
    # Create outliers section (if key is not missing)
    if 'outliers' in reports:
        lines.extend(_generate_outliers_section(reports['outliers'])) # Add returned list of _generate_outliers_section() to lines
    
    # Create structural errors section (if key is not missing)
    if 'structural_errors' in reports:
        lines.extend(_generate_structural_errors_section(reports['structural_errors'])) # Add returned list of _generate_structural_errors_section() to lines
    
    # Create postprocessing section (if key is not missing)
    if 'postprocessing' in reports:
        lines.extend(_generate_postprocessing_section(reports['postprocessing'])) # Add returned list of _generate_postprocessing_section() to lines
    
    # Write md file and save it to filepath
    file = open(filepath, 'w') # Create file @filepath (if already exists -> gets cleared)
    file.write('\n'.join(lines)) # Write the joined string into file 
    # Note: '\n'.join(lines) joins all elements of lines to a string with each element seperated by \n
    file.close() # Close and save the file 

    # Terminal output: end
    print("✓")

# ============================================================================
# Section Generators (Private)
# ============================================================================

def _generate_summary(reports: dict) -> list:
    """Generate summary section"""
    
    # Initialize list of lines
    lines = []

    # Create title
    lines.append("---") # divider line 
    lines.append("") # empty line 
    lines.append("## Summary")
    lines.append("") # empty line
    
    # Get shape info from preprocessing (if available)
    if 'preprocessing' in reports:
        report_pre = reports['preprocessing']
        lines.append(f"- **Original shape:** {report_pre['original_shape'][0]} rows × {report_pre['original_shape'][1]} columns")
        lines.append(f"- **Shape after preprocessing:** {report_pre['final_shape'][0]} rows × {report_pre['final_shape'][1]} columns")
    
    # Get values of key changes (if available)
    total_rows_deleted = 0
    total_imputations = 0
    total_outliers = 0
    total_values_changed = 0

    if 'duplicates' in reports:
        total_rows_deleted += reports['duplicates']['rows_removed']

    if 'missing_values' in reports:
        total_rows_deleted += reports['missing_values']['rows_deleted']
        total_imputations = len(reports['missing_values']['imputations_num']) + len(reports['missing_values']['imputations_categ'])

    if 'datetime' in reports:
        total_rows_deleted += reports['datetime']['rows_deleted']
    
    if 'outliers' in reports:
        total_rows_deleted += reports['outliers']['rows_deleted']
        total_outliers = reports['outliers']['total_outliers']
    
    if 'structural_errors' in reports:
        report_str = reports['structural_errors']
        total_values_changed = 0

        # Distinguish if Structural_Error.py was applied multiple times or just once
        # Multiple times if report_str = list (of dict), otherwise single time
        if isinstance(report_str, list):
            # Note isinstance(x, y) returns true if object x corresponds to type y 
            for single_report_str in report_str:
                total_values_changed += single_report_str['values_changed']

        else:
            total_values_changed = report_str['values_changed']
    
    if total_rows_deleted > 0:
        lines.append(f"- **Total rows deleted:** {total_rows_deleted}")

    if total_imputations > 0:
        lines.append(f"- **Total values imputed:** {total_imputations}")

    if total_outliers > 0:
        lines.append(f"- **Total outliers handled:** {total_outliers}")
        
    if total_values_changed > 0:
        lines.append(f"- **Total structural errors fixed:** {total_values_changed}")
    
    lines.append("") # empty line

    return lines

def _generate_preprocessing_section(report: dict) -> list:
    """Generate preprocessing section"""

    # Initialize list of lines
    lines = []

    # Create title 
    lines.append("---") # divider line 
    lines.append("") # empty line 
    lines.append("## Preprocessing")
    lines.append("") # empty line 
    
    # Get info about removed rows / columns (if available)
    if report['rows_removed'] > 0:
        lines.append(f"- **Completely empty rows removed:** {report['rows_removed']}")
    if report['cols_removed'] > 0:
        lines.append(f"- **Completely empty columns removed:** {report['cols_removed']}")
    
    # Get info about renamed columns (if available)
    columns_renamed = report['columns_renamed']
    if len(columns_renamed) > 0:
        lines.append(f"- **Number of columns renamed:** {len(columns_renamed)}")
        lines.append("") # empty line

        # Create table with original & new column names 
        lines.append("| Original Column Name | New Column Name |")
        lines.append("|----------------------|-----------------|")
        for column_renamed in columns_renamed:
            lines.append(f"| {column_renamed['old']} | {column_renamed['new']} |")
    
    lines.append("") # empty line 

    return lines

def _generate_duplicates_section(report: dict) -> list:
    """Generate duplicates section"""
    
    # Initialize list of lines
    lines = []

    # Create title
    lines.append("---") # divider line 
    lines.append("") # empty line
    lines.append("## Duplicates")
    lines.append("") # empty line 
    
    # Get info about duplicates 
    rows_removed = report['rows_removed']
    cols_removed = report['cols_removed']
    
    if rows_removed == 0 and cols_removed == 0:
        lines.append("No duplicate rows or duplicate columns found.")

    else:
        if rows_removed > 0:
            lines.append(f"- **Duplicate rows removed:** {rows_removed}")

        if cols_removed > 0:
            lines.append(f"- **Duplicate columns removed:** {cols_removed}")
    
    lines.append("") # empty line

    return lines

def _generate_missing_values_section(report: dict) -> list:
    """Generate missing values section"""
    
    # Initialize list of lines
    lines = []

    # Create title
    lines.append("---") # divider line
    lines.append("") # empty line
    lines.append("## Missing Values")
    lines.append("") # empty line 
    
    # Create section about selected columns for which missing values were handled
    if 'columns' in report: 
        lines.append(f"### Column Selection")
        lines.append("") # empty line
        lines.append(f"**Selected columns**: ")

        for column in report['columns']: 
            lines.append(f"- {column}")

        lines.append("") # empty line 
        lines.append("**Note:** Only these columns were selected to handle missing values.")
        lines.append("") # empty line 
    
    else:
        lines.append("### Column Selection")
        lines.append("") # empty line
        lines.append("All columns were selected to handle missing values.")
        lines.append("") # empty line

    # Create section with most important facts (Overview)
    lines.append("### Overview")
    lines.append("") # empty line

    num_missing_before = report['num_missing_before']
    categ_missing_before = report['categ_missing_before']

    if num_missing_before == 0 and categ_missing_before == 0:
        lines.append("No missing values found.")
        lines.append("") # empty line
        return lines

    lines.append(f"- **Numerical missing values:** {num_missing_before}")
    lines.append(f"- **Categorical missing values:** {categ_missing_before}")
    lines.append(f"- **Chosen method for numerical missing values:** {report['method_num']}")
    lines.append(f"- **Chosen method for categorical missing values:** {report['method_categ']}")

    if report['rows_deleted'] > 0:
        lines.append(f"- **Rows deleted:** {report['rows_deleted']}")
    
    # Create section with table of imputations 
    imputations_num = report['imputations_num']
    imputations_categ = report['imputations_categ']

    if len(imputations_num) > 0 or len(imputations_categ) > 0:
        lines.append("") # empty line
        lines.append("### Imputations")
        lines.append("") # empty line

        if len(imputations_num) > 0:
            lines.append("**Numerical:**")
            lines.append("| Row | Column | New Value | Method |")
            lines.append("|-----|--------|-----------|--------|")
            for imp in imputations_num:
                lines.append(f"| {imp['row']} | {imp['column']} | {imp['new_value']} | {imp['method']} |")
        
        lines.append("") # empty line

        if len(imputations_categ) > 0:
            lines.append("**Categorical:**")
            lines.append("| Row | Column | New Value | Method |")
            lines.append("|-----|--------|-----------|--------|")
            for imp in imputations_categ:
                lines.append(f"| {imp['row']} | {imp['column']} | {imp['new_value']} | {imp['method']} |")
                
    lines.append("") # empty line

    return lines

def _generate_datetime_section(report: dict) -> list:
    """Generate datetime standardization section"""
    
    # Initialize list of lines
    lines = []

    # Create title
    lines.append("---") # divider line
    lines.append("") # empty line
    lines.append("## DateTime Standardization")
    lines.append("") # empty line
    
    # Get most important facts (if available)
    lines.append(f"- **Column:** {report['column']}")
    lines.append(f"- **Format:** {report['format']}")
    lines.append(f"- **Invalid handling:** {report['handle_invalid']}")
    lines.append(f"- **Total values:** {report['total_values']}")
    lines.append(f"- **Successfully converted / standardized:** {report['n_standardized_dates']}")
    lines.append(f"- **Invalid values:** {report['invalid']}")
    
    if report['rows_deleted'] > 0:
        lines.append(f"- **Rows deleted:** {report['rows_deleted']}")
    
    # Create table, to show how invalid values were handled
    if report['invalid'] > 0:
        details_invalid = report['details_invalid']

        lines.append("") # empty line
        lines.append("### Invalid values handled")
        lines.append("") # empty line

        lines.append("| Row | Original | Action |")
        lines.append("|-----|----------|--------|")

        for detail_invalid in details_invalid: 
            lines.append(f"| {detail_invalid['row']} | {detail_invalid['original']} | {detail_invalid['action']} |")
    
    lines.append("") # empty line

    return lines

def _generate_outliers_section(report: dict) -> list:
    """Generate outliers section"""
    
    # Initialize list of lines
    lines = []

    # Create title
    lines.append("---") # divider line
    lines.append("") # empty line
    lines.append("## Outliers")
    lines.append("") # empty line

    # End outlier section, if no numerical columns found
    if len(report['column_bounds']) == 0: 
        lines.append("No numerical columns found in dataset.")
        lines.append("") # empty line 
        return lines

    # Create table with lower & upper bounds for each numerical column 
    lines.append("### Lower & Upper Bounds")
    lines.append("") # empty line

    lines.append("| Column | Lower Bound | Upper Bound |")
    lines.append("|--------|-------------|-------------|")

    for column_bound in report['column_bounds']:
        # Round the bounds to same precision in decimal digits
        lower_bound = round(column_bound['lower_bound'], 4)
        upper_bound = round(column_bound['upper_bound'], 4)
        lines.append(f"| {column_bound['column']} | {lower_bound} | {upper_bound} |")

    # Create overview for outliers (if available)
    lines.append("") # empty line
    lines.append("### Overview")
    lines.append("") # empty line
    
    if report['total_outliers'] == 0:
        lines.append(f"No outliers found with multiplier {report['multiplier']}.")
        lines.append("") # empty line
        return lines
    
    lines.append(f"- **Multiplier:** {report['multiplier']}")
    lines.append(f"- **Total outliers:** {report['total_outliers']}")
    lines.append(f"- **Method:** {report['method']}")
    
    if report['rows_deleted'] > 0:
        lines.append(f"- **Rows deleted:** {report['rows_deleted']}")
    
    # Create table which shows how outliers were handled 
    lines.append("") # empty line
    lines.append("### Outliers Handled")
    lines.append("") # empty line

    lines.append("| Row | Column | Original | New Value | Bound |")
    lines.append("|-----|--------|----------|-----------|-------|")

    if report['method'] == 'winsorize': 
        for outlier in report['outliers']:
            # Round original & new value to same precision in decimal digits (Note: In pipeline rounding is applied to df in post-processing)
            original_value = round(outlier['original_value'], 4)
            new_value = round(outlier['new_value'], 4)

            lines.append(f"| {outlier['row']} | {outlier['column']} | {original_value} | {new_value} | {outlier['bound']} |")
    
    if report['method'] == 'delete': 
        for outlier in report['outliers']:
            # Round original value
            original_value = round(outlier['original_value'], 4)

            lines.append(f"| {outlier['row']} | {outlier['column']} | {original_value} | {outlier['new_value']} | {outlier['bound']} |")
    
    lines.append("") # empty line

    return lines

def _generate_structural_errors_section(report) -> list:
    """Generate structural errors section"""
    
    # Initialize list of lines
    lines = []

    lines.append("---") # divider line
    lines.append("") # empty line
    lines.append("## Structural Errors")
    lines.append("") # empty line
    
    # Distinguish if structural errors was applied once or multiple times
    if isinstance(report, dict):
        # Note isinstance(x, y) returns true if object x corresponds to type y
        
        # Create overview for structural errors 
        lines.append("") # empty line
        lines.append("## Overview")
        lines.append("") # empty line 

        lines.append(f"- **Column processed:** {report['column']}")

        lines.append(f"- **Similarity method:** {report['similarity']}")
        # Show embedding model if embeddings were used
        if report['similarity'] == 'embeddings':
            lines.append(f"- **Embedding model:** {report['embedding_model']}")

        lines.append(f"- **Clustering method:** {report['clustering']}")
        # Show relevant parameter based on clustering method
        if report['clustering'] == 'hierarchical':
            lines.append(f"- **Threshold (hierarchical):** {report['threshold_h']}")
        elif report['clustering'] == 'connected_components':
            lines.append(f"- **Threshold (connected components):** {report['threshold_cc']}")
        else: 
            lines.append(f"- **Damping (affinity propagation):** {report['damping']}")
        
        lines.append(f"- **Canonical selection:** {report['canonical']}")
        
        lines.append(f"- **Values changed:** {report['values_changed']}")
        lines.append(f"- **Unique values before:** {report['unique_values_before']}")
        lines.append(f"- **Unique values after:** {report['unique_values_after']}")
        change_unique_values = round((report['unique_values_after'] / report['unique_values_before']) * 100, 2)
        lines.append(f"- **Change in unique values:** {change_unique_values}%")

        if report['unique_values_before'] == report['unique_values_after']: 
            lines.append("") # empty line
            lines.append(f"No clustering was applied, as only one unique value exists.")
            lines.append("") # empty line

            return lines
        else:
            # Create section with table which shows clustering results 
            lines.append("") # empty line
            lines.append("#### Clustering Results")
            lines.append("") # empty line 

            mapping = report['mapping']
            clusters = {}

            # Get dict of clusters (key: canonical name, value: list of unique values corresponding to canonical name)
            for original, canonical in mapping.items():
                if canonical not in clusters:
                    clusters[canonical] = []
                clusters[canonical].append(original)
    
            lines.append("| Original Values | Clustered to Canonical |")
            lines.append("|-----------------|------------------------|")

            for canonical, originals in clusters.items():
                originals_str = "; ".join(originals)
                # Note: '; '.join(originals) joins all elements of originals to a string with each element seperated by ;
                lines.append(f"| {originals_str} | {canonical} |")

            lines.append("") # empty line 

            return lines
        
    else:
        # Create overview for structural errors 
        lines.append("") # empty line
        lines.append("## Overview")
        lines.append("") # empty line

        # Calculate totals across all single reports
        total_values_changed = 0
        total_unique_values_before = 0
        total_unique_values_after = 0 
        for single_report in report:
            total_values_changed += single_report['values_changed']
            total_unique_values_before += single_report['unique_values_before']
            total_unique_values_after += single_report['unique_values_after']

        total_columns = len(report)

        lines.append(f"- **Columns processed:** {total_columns}")
        lines.append(f"- **Total values changed:** {total_values_changed}")
        lines.append(f"- **Total unique values before:** {total_unique_values_before}")
        lines.append(f"- **Total unique values after:** {total_unique_values_after}")
        total_change_unique_values = round((total_unique_values_after / total_unique_values_before) * 100, 2)
        lines.append(f"- **Total change in unique values:** {total_change_unique_values}%")
        lines.append("")

        # Generate section for each column processed
        for single_report in report:
            lines.append(f"### Column: {single_report['column']}")
            lines.append("")
            
            lines.append(f"- **Similarity method:** {single_report['similarity']}")
            # Show embedding model if embeddings were used
            if single_report['similarity'] == 'embeddings':
                lines.append(f"- **Embedding model:** {single_report['embedding_model']}")

            lines.append(f"- **Clustering method:** {single_report['clustering']}")
            # Show relevant parameter based on clustering method
            if single_report['clustering'] == 'hierarchical':
                lines.append(f"- **Threshold (hierarchical):** {single_report['threshold_h']}")
            elif single_report['clustering'] == 'connected_components':
                lines.append(f"- **Threshold (connected components):** {single_report['threshold_cc']}")
            else: 
                lines.append(f"- **Damping (affinity propagation):** {single_report['damping']}")
        

            lines.append(f"- **Canonical selection:** {single_report['canonical']}")
            
            lines.append(f"- **Values changed:** {single_report['values_changed']}")
            lines.append(f"- **Unique values before:** {single_report['unique_values_before']}")
            lines.append(f"- **Unique values after:** {single_report['unique_values_after']}")
            change_unique_values = round((single_report['unique_values_after'] / single_report['unique_values_before']) * 100, 2)
            lines.append(f"- **Change in unique values:** {change_unique_values}%")

            if single_report['unique_values_before'] == single_report['unique_values_after']: 
                lines.append("") # empty line
                lines.append(f"No clustering was applied, as only one unique value in column '{single_report['column']}' exists.")
                lines.append("") # empty line
            
            else:
                # Create section with table which shows clustering results 
                lines.append("") # empty line
                lines.append("#### Clustering Results")
                lines.append("") # empty line 

                mapping = single_report['mapping']
                clusters = {}

                # Get dict of clusters (key: canonical name, value: list of unique values corresponding to canonical name)
                for original, canonical in mapping.items():
                    if canonical not in clusters:
                        clusters[canonical] = []
                    clusters[canonical].append(original)
        
                lines.append("| Original Values | Clustered to Canonical |")
                lines.append("|-----------------|------------------------|")

                for canonical, originals in clusters.items():
                    originals_str = "; ".join(originals)
                    # Note: '; '.join(originals) joins all elements of originals to a string with each element seperated by ;
                    lines.append(f"| {originals_str} | {canonical} |")

                lines.append("") # empty line 

        return lines

def _generate_postprocessing_section(report: dict) -> list:
    """Generate postprocessing section"""
    # Initialize list of lines
    lines = []

    lines.append("---") # divider line
    lines.append("") # empty line
    lines.append("## Postprocessing")
    lines.append("") # empty line 
    
    # Get table of changes applied in post-processing (if available)
    changes = report['changes']

    if len(changes) > 0:
        lines.append("| Column | Action |")
        lines.append("|--------|--------|")

        for change in changes:
            lines.append(f"| {change['column']} | {change['action']} |")

    else:
        lines.append("No postprocessing changes applied.")
    
    lines.append("") # empty line 
    
    return lines