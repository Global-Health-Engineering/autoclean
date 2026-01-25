"""
Generate cleaning report as markdown file

This function gets as an input a dictionary, consisting of every single report of each cleaning function, 
which was applied in the pipeline. Note each single report is again a dictionary. With this input a comprehensive 
report file (md file) is generated. 

Input (needs to have this structure):
    reports = {'preprocessing': report_pre,
               'duplicates': report_dup,
               'semantic_outliers': report_sem,
               'outliers': report_out,
               'datetime': report_date,
               'structural_errors': report_str,
               'missing_values': report_miss,
               'postprocessing': report_post}

Note: 
    - Only include reports for cleaning functions that were actually performed (missing keys will be skipped in the report)
    - Value of key 'structural_errors' can be a list of dictionaries, if Structural_Errors.py was applied multiple times
    - Value of key 'semantic_outliers' can be a list of dictionaries, if Semantic_Outliers.py was applied multiple times
    - Value of key 'missing_values' can be a list of dictionaries, if Missing_values.py was applied multiple times

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

# Imported libraries
from datetime import datetime

def generate_cleaning_report(reports: dict, report_filepath: str = 'Cleaning_Report.md', dataset_name: str = None) -> None:
    """
    Generate Markdown cleaning report from report dicts.
    
    Parameters:
        report_filepath: Output path for Markdown file (default = 'Cleaning_Report.md')
        dataset_name: Optional name of dataset for report (default = None)
    
    Returns:
        Function returns nothing (None), directly saves md file in desired location (report_filepath)
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
        lines.append(f"**Name of dataset:** {dataset_name}  ")

    lines.append(f"**Filepath of messy dataset:** {reports['preprocessing']['input_filepath']}  ")
    lines.append(f"**Filepath of cleaned dataset:** {reports['postprocessing']['output_filepath']}  ")
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
    
    # Create semantic outliers section (if key is not missing)
    if 'semantic_outliers' in reports:
        lines.extend(_generate_semantic_outliers_section(reports['semantic_outliers'])) # Add returned list of _generate_semantic_outliers_section() to lines

    # Create outliers section (if key is not missing)
    if 'outliers' in reports:
        lines.extend(_generate_outliers_section(reports['outliers'])) # Add returned list of _generate_outliers_section() to lines

    # Create datetime section (if key is not missing)
    if 'datetime' in reports:
        lines.extend(_generate_datetime_section(reports['datetime'])) # Add returned list of _generate_datetime_section() to lines

    # Create structural errors section (if key is not missing)
    if 'structural_errors' in reports:
        lines.extend(_generate_structural_errors_section(reports['structural_errors'])) # Add returned list of _generate_structural_errors_section() to lines

    # Create missing values section (if key is not missing)
    if 'missing_values' in reports:
        lines.extend(_generate_missing_values_section(reports['missing_values'])) # Add returned list of _generate_missing_values_section() to lines
        
    # Create postprocessing section (if key is not missing)
    if 'postprocessing' in reports:
        lines.extend(_generate_postprocessing_section(reports['postprocessing'])) # Add returned list of _generate_postprocessing_section() to lines
    
    # Write md file and save it to report_filepath
    file = open(report_filepath, 'w') # Create file @report_filepath (if already exists -> gets cleared)
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
    if 'preprocessing' in reports and 'postprocessing' in reports:
        report_pre = reports['preprocessing']
        report_post = reports['postprocessing']
        lines.append(f"- **Original shape:** {report_pre['original_shape'][0]} rows × {report_pre['original_shape'][1]} columns")
        lines.append(f"- **Final shape:** {report_post['final_shape'][0]} rows × {report_post['final_shape'][1]} columns")
    
    # Get values of key changes (if available)
    total_rows_deleted = 0
    total_cols_deleted = 0 
    total_imputations = 0
    total_outliers = 0
    total_values_changed = 0
    total_semantic_outliers = 0
    
    if 'preprocessing' in reports:
        total_rows_deleted += reports['preprocessing']['rows_removed']
        total_cols_deleted += reports['preprocessing']['cols_removed']

    if 'duplicates' in reports:
        total_rows_deleted += reports['duplicates']['rows_removed']
        total_cols_deleted += reports['duplicates']['cols_removed']

    if 'datetime' in reports:
        total_rows_deleted += reports['datetime']['rows_deleted']
    
    if 'outliers' in reports:
        total_rows_deleted += reports['outliers']['rows_deleted']
        total_outliers = reports['outliers']['total_outliers']
    
    if 'missing_values' in reports:
        report_miss = reports['missing_values']

        # Distinguish if Missing_Values.py was applied multiple times or just once
        # Multiple times if report_miss = list (of dict), otherwise single time
        if isinstance(report_miss, list):
            # Note isinstance(x, y) returns true if object x corresponds to type y
            for single_report in report_miss:
                total_rows_deleted += single_report['n_rows_deleted']
                total_imputations += single_report['n_imputed']

        else:
            total_rows_deleted += report_miss['n_rows_deleted']
            total_imputations += report_miss['n_imputed']

    if 'structural_errors' in reports:
        report_str = reports['structural_errors']

        # Distinguish if Structural_Error.py was applied multiple times or just once
        # Multiple times if report_str = list (of dict), otherwise single time
        if isinstance(report_str, list):
            # Note isinstance(x, y) returns true if object x corresponds to type y 
            for single_report_str in report_str:
                total_values_changed += single_report_str['values_changed']

        else:
            total_values_changed = report_str['values_changed']

    if 'semantic_outliers' in reports:
        report_sem = reports['semantic_outliers']
        
        # Distinguish if Semantic_Outliers.py was applied multiple times or just once
        # Multiple times if report_sem = list (of dict), otherwise single time
        if isinstance(report_sem, list):
            for single_report_sem in report_sem:
                # Note isinstance(x, y) returns true if object x corresponds to type y 
                total_semantic_outliers += single_report_sem['outliers_detected']
                total_rows_deleted += single_report_sem['rows_deleted']
        else:
            total_semantic_outliers = report_sem['outliers_detected']
            total_rows_deleted += report_sem['rows_deleted']

    lines.append(f"- **Total rows deleted:** {total_rows_deleted}")
    lines.append(f"- **Total columns deleted:** {total_cols_deleted}")    
    lines.append(f"- **Total values imputed:** {total_imputations}")
    lines.append(f"- **Total outliers handled:** {total_outliers}")
    lines.append(f"- **Total semantic outliers detected:** {total_semantic_outliers}")
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

    # Get info about additional values handled as missing, removed rows & columns (if available)
    if 'additional_na_values' in report:
        lines.append(f"- **Additional values handled as missing in inport:** {'; '.join(report['additional_na_values'])}")
        # Note: '; '.join(report['additional_n_values']) joins all elements of report['additional_n_values'] to a string with each element seperated by ;

    if report['rows_removed'] > 0:
        lines.append(f"- **Completely empty rows removed:** {report['rows_removed']}")

    if report['cols_removed'] > 0:
        lines.append(f"- **Completely empty columns removed:** {report['cols_removed']}")
        
    if report['rows_removed'] == 0 and report['cols_removed'] == 0: 
        lines.append("No completely empty rows or columns found respectfully removed.")

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

def _generate_semantic_outliers_section(report) -> list:
    """Generate semantic outliers section"""
    
    # Initialize list of lines
    lines = []
    
    lines.append("---") # divider line
    lines.append("") # empty line
    lines.append("## Semantic Outliers")

    # Distinguish if semantic outliers was applied once or multiple times
    if isinstance(report, dict):
        # Note isinstance(x, y) returns true if object x corresponds to type y

        # Create overview for semantic outliers
        lines.append("") # empty line
        lines.append("### Overview")
        lines.append("") # empty line 
        
        lines.append(f"- **Column processed:** {report['column']}")
        lines.append(f"- **Given context:** {report['context']}")
        lines.append(f"- **Threshold:** {report['threshold']}")
        lines.append(f"- **Action:** {report['action']}")
        lines.append(f"- **Unique values checked:** {report['unique_values_checked']}")
        lines.append(f"- **Outliers detected:** {report['outliers_detected']}")
        
        if report['rows_deleted'] > 0:
            lines.append(f"- **Rows deleted:** {report['rows_deleted']}")
        
        # Create table of detected outliers (if available)
        if report['outliers_detected'] > 0:
            lines.append("") # empty line
            lines.append("#### Detected Outliers")
            lines.append("") # empty line

            lines.append("| Value | Confidence | Number of affected rows |")
            lines.append("|-------|------------|-------------------------|")
            
            for outlier in report['outliers']:
                lines.append(f"| {outlier['value']} | {outlier['confidence']} | {outlier['n_affected_rows']} |")
        
        lines.append("") # empty line
        return lines
    
    else:
         # Create overview for semantic outliers
        lines.append("") # empty line
        lines.append("### Overview")
        lines.append("") # empty line
        
        # Calculate totals across all single reports
        total_outliers = 0
        total_rows_affected = 0
        for single_report in report:
            total_outliers += single_report['outliers_detected']
            total_rows_affected += single_report['rows_affected']
        
        lines.append(f"- **Columns processed:** {len(report)}")
        lines.append(f"- **Total outliers detected:** {total_outliers}")
        lines.append(f"- **Total number of affected rows:** {total_rows_affected}")
        lines.append("") # empty line
        
        # Generate section for each column processed
        for single_report in report:
            lines.append(f"### Column: {single_report['column']}")
            lines.append("") # empty line
            
            lines.append(f"- **Given context:** {single_report['context']}")
            lines.append(f"- **Threshold:** {single_report['threshold']}")
            lines.append(f"- **Action:** {single_report['action']}")
            lines.append(f"- **Unique values checked:** {single_report['unique_values_checked']}")
            lines.append(f"- **Outliers detected:** {single_report['outliers_detected']}")
            
            if single_report['rows_deleted'] > 0:
                lines.append(f"- **Rows deleted:** {single_report['rows_deleted']}")
            
            # Create table of detected outliers (if available)
            if single_report['outliers_detected'] > 0:
                lines.append("") # empty line
                lines.append("#### Detected Outliers")
                lines.append("") # empty line

                lines.append("| Value | Confidence | Number of affected rows |")
                lines.append("|-------|------------|-------------------------|")
                
                for outlier in single_report['outliers']:
                    lines.append(f"| {outlier['value']} | {outlier['confidence']} | {outlier['n_affected_rows']} |")
            
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

    lines.append("| Column | Original | New Value | Bound |")
    lines.append("|--------|----------|-----------|-------|")

    if report['method'] == 'winsorize': 
        for outlier in report['outliers']:
            lines.append(f"| {outlier['column']} | {outlier['original_value']} | {outlier['new_value']} | {outlier['bound']} |")

        lines.append("") # empty line
        lines.append("**Note:** New values shown above are pre-rounding. Final values may be rounded in post-processing to match original column precision.")
    
    if report['method'] == 'delete': 
        for outlier in report['outliers']:
            lines.append(f"| {outlier['column']} | {outlier['original_value']} | {outlier['new_value']} | {outlier['bound']} |")
    
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

        lines.append("| Original | Action |")
        lines.append("|----------|--------|")

        for detail_invalid in details_invalid: 
            lines.append(f"| {detail_invalid['original']} | {detail_invalid['action']} |")
    
    lines.append("") # empty line

    return lines

def _generate_structural_errors_section(report) -> list:
    """Generate structural errors section"""
    
    # Initialize list of lines
    lines = []

    lines.append("---") # divider line
    lines.append("") # empty line
    lines.append("## Structural Errors")
    
    # Distinguish if structural errors was applied once or multiple times
    if isinstance(report, dict):
        # Note isinstance(x, y) returns true if object x corresponds to type y
        
        # Create overview for structural errors 
        lines.append("") # empty line
        lines.append("### Overview")
        lines.append("") # empty line 

        lines.append(f"- **Column processed:** {report['column']}")

        lines.append(f"- **Similarity method:** {report['similarity']}")
        # Show embedding model if embeddings were used
        if report['similarity'] == 'embeddings':
            lines.append(f"- **Embedding model:** {report['embedding_model']}")
        # Show LLM settings if LLM similarity was used
        elif report['similarity'] == 'llm':
            lines.append(f"- **LLM mode:** {report['llm_mode']}")
            lines.append(f"- **LLM context provided:** {report['llm_context']}")

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

        if report['unique_values_before'] == report['unique_values_after']: 
            if report['unique_values_before'] == 1:
                lines.append("") # empty line
                lines.append(f"No clustering was applied, as only one unique value exists.")
                lines.append("") # empty line

                return lines
            
            else:
                lines.append("") # empty line
                lines.append(f"No clustering was applied (number of unique values have not changed).")
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
        lines.append("### Overview")
        lines.append("") # empty line

        # Calculate totals across all single reports
        total_values_changed = 0
        total_unique_values_before = 0
        total_unique_values_after = 0 
        for single_report in report:
            total_values_changed += single_report['values_changed']
            total_unique_values_before += single_report['unique_values_before']
            total_unique_values_after += single_report['unique_values_after']

        lines.append(f"- **Columns processed:** {len(report)}")
        lines.append(f"- **Total values changed:** {total_values_changed}")
        lines.append(f"- **Total unique values before:** {total_unique_values_before}")
        lines.append(f"- **Total unique values after:** {total_unique_values_after}")
        lines.append("") # empty line

        # Generate section for each column processed
        for single_report in report:
            lines.append(f"### Column: {single_report['column']}")
            lines.append("")
            
            lines.append(f"- **Similarity method:** {single_report['similarity']}")
            # Show embedding model if embeddings were used
            if single_report['similarity'] == 'embeddings':
                lines.append(f"- **Embedding model:** {single_report['embedding_model']}")
            # Show LLM settings if LLM similarity was used
            elif single_report['similarity'] == 'llm':
                lines.append(f"- **LLM mode:** {single_report['llm_mode']}")
                lines.append(f"- **LLM context provided:** {single_report['llm_context']}")

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
            
            if single_report['unique_values_before'] == single_report['unique_values_after']: 
                if single_report['unique_values_before'] == 1:
                    lines.append("") # empty line
                    lines.append(f"No clustering was applied, as only one unique value exists.")
                    lines.append("") # empty line

                    return lines
            
                else:
                    lines.append("") # empty line
                    lines.append(f"No clustering was applied (number of unique values have not changed).")
                    lines.append("") # empty line
                    
                    return lines
            
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

def _generate_missing_values_section(report) -> list:
    """Generate missing values section"""
    
    # Initialize list of lines
    lines = []
    
    lines.append("---") # divider line
    lines.append("") # empty line
    lines.append("## Missing Values")

    # Distinguish if missing values was applied once or multiple times
    if isinstance(report, dict):
        # Note isinstance(x, y) returns true if object x corresponds to type y

        # Create overview for missing values
        lines.append("") # empty line
        lines.append("### Overview")
        lines.append("") # empty line
        
        lines.append(f"- **Column processed:** {report['column']}")
        lines.append(f"- **Method:** {report['method']}")

        # Get features columns & parameters if KNN/MissForest was used 
        if report['method'] in ['knn', 'missforest']:
            if report['features'] != None:
                lines.append(f"- **Features used:** {'; '.join(report['features'])}")
                # Note: '; '.join(report['features']) joins all elements of report['features'] to a string with each element seperated by ;
            else:
                lines.append(f"- **Features used:** All columns, except column '{report['column']}'")
            
            if report['method'] == 'knn':
                lines.append(f"- **n_neighbors:** {report['n_neighbors']}")

            elif report['method'] == 'missforest':
                lines.append(f"- **n_estimators:** {report['n_estimators']}")
                lines.append(f"- **max_iter:** {report['max_iter']}")
                lines.append(f"- **max_depth:** {report['max_depth']}")
                lines.append(f"- **min_samples_leaf:** {report['min_samples_leaf']}")

        lines.append(f"- **Missing values before imputation:** {report['n_missing_before']}")
        
        if report['n_rows_deleted'] > 0:
            lines.append(f"- **Rows deleted:** {report['n_rows_deleted']}")
        else:
            lines.append(f"- **Values imputed:** {report['n_imputed']}")
             
        # Create table of imputations (if available)
        if report['n_imputed'] > 0:
            lines.append("") # empty line
            lines.append("#### Imputations")
            lines.append("") # empty line

            lines.append("| Row | New imputed Value |")
            lines.append("|-----|-------------------|")

            for imp in report['imputations']:
                lines.append(f"| {imp['row'] + 1} | {imp['new_value']} |")
            
            lines.append("") # empty line
            lines.append("**Note:** Imputed values shown above are pre-rounding. Final values may be rounded in post-processing.")
        
        lines.append("") # empty line

        return lines
    
    else:
        # Create overview for missing values
        lines.append("") # empty line
        lines.append("### Overview")
        lines.append("") # empty line
        
        # Calculate totals across all single reports
        total_imputed = 0
        total_rows_deleted = 0
        for single_report in report:
            total_imputed += single_report['n_imputed']
            total_rows_deleted += single_report['n_rows_deleted']
        
        lines.append(f"- **Columns processed:** {len(report)}")
        lines.append(f"- **Total values imputed:** {total_imputed}")
        lines.append(f"- **Total rows deleted:** {total_rows_deleted}")
        lines.append("") # empty line
        
        # Generate section for each column processed
        for single_report in report:
            lines.append(f"### Column: {single_report['column']}")
            lines.append("") # empty line
            
            lines.append(f"- **Method:** {single_report['method']}")

            # Get features columns & parameters if KNN/MissForest was used 
            if single_report['method'] in ['knn', 'missforest']:
                if single_report['features'] != None:
                    lines.append(f"- **Features used:** {'; '.join(single_report['features'])}")
                    # Note: '; '.join(report['features']) joins all elements of report['features'] to a string with each element seperated by ;
                else:
                    lines.append(f"- **Features used:** All columns, except column '{single_report['column']}'")
                
                if single_report['method'] == 'knn':
                    lines.append(f"- **n_neighbors:** {single_report['n_neighbors']}")

                elif single_report['method'] == 'missforest':
                    lines.append(f"- **n_estimators:** {single_report['n_estimators']}")
                    lines.append(f"- **max_iter:** {single_report['max_iter']}")
                    lines.append(f"- **max_depth:** {single_report['max_depth']}")
                    lines.append(f"- **min_samples_leaf:** {single_report['min_samples_leaf']}")

            lines.append(f"- **Missing values before imputation:** {single_report['n_missing_before']}")
        
            if single_report['n_rows_deleted'] > 0:
                lines.append(f"- **Rows deleted:** {single_report['n_rows_deleted']}")
            else:
                lines.append(f"- **Values imputed:** {single_report['n_imputed']}")
            
            # Create table of imputations (if available)
            if single_report['n_imputed'] > 0:
                lines.append("") # empty line
                lines.append("#### Imputations")
                lines.append("") # empty line

                lines.append("| Row | New imputed Value |")
                lines.append("|-----|-------------------|")
                
                for imp in single_report['imputations']:
                    lines.append(f"| {imp['row'] + 1} | {imp['new_value']} |")
                
                lines.append("") # empty line
                lines.append("**Note:** Imputed values shown above are pre-rounding. Final values may be rounded in post-processing.")
        
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
    
    if 'output_missing_values' in report:
        lines.append(f"**Chosen output format of missing values (np.nan):** {report['output_missing_values']}")
    
    # Get table of precision restoration (rounding) applied in post-processing (if available)
    changes = report['changes']

    lines.append("### Precision Restoration (rounding)")
    lines.append("") # empty line 

    if len(changes) > 0:
        lines.append("| Column | Action |")
        lines.append("|--------|--------|")

        for change in changes:
            lines.append(f"| {change['column']} | {change['action']} |")

    else:
        lines.append("No precision restoration (rounding) was applied in post-processing.")

    # Create table of renamed columns (if available)
    lines.append("") # empty line 
    lines.append("### Renamed Columns")
    lines.append("") # empty line 

    columns_renamed = report['columns_renamed']

    if len(columns_renamed) > 0:
        # Create table with original & new column names 
        lines.append("| Original Column Name | New Column Name |")
        lines.append("|----------------------|-----------------|")
        for column_renamed in columns_renamed:
            lines.append(f"| {column_renamed['old']} | {column_renamed['new']} |")
    else: 
        lines.append("Column renaming was not applied.")

    lines.append("") # empty line 
    
    return lines