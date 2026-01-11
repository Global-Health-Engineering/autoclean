# Imported libraries
from datetime import datetime

"""
Generate Markdown cleaning report from all report dicts

This function takes the report dicts from each cleaning function
and generates a comprehensive Markdown report file.

Usage:
    reports = {
        'preprocessing': preprocess_report,
        'duplicates': duplicates_report,
        'missing_values': missing_report,
        'datetime': datetime_report,
        'outliers': outliers_report,
        'structural_errors': structural_errors_report,
        'postprocessing': postprocess_report
    }
    generate_cleaning_report(reports, 'cleaning_report.md')

Note: Only include reports for steps that were actually performed.
      Missing keys will be skipped in the report.
"""


def generate_cleaning_report(reports: dict, 
                              filepath: str = 'cleaning_report.md',
                              dataset_name: str = None) -> None:
    """
    Generate Markdown cleaning report from report dicts.
    
    Parameters:
        reports: Dict containing report dicts from each cleaning function
        filepath: Output path for Markdown file (default: 'cleaning_report.md')
        dataset_name: Optional name of dataset for report title
    """
    
    lines = []
    
    # Header
    lines.append("# AutoClean Report")
    lines.append("")
    if dataset_name:
        lines.append(f"**Dataset:** {dataset_name}")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    # Summary section
    lines.extend(_generate_summary(reports))
    
    # Preprocessing section
    if 'preprocessing' in reports:
        lines.extend(_generate_preprocessing_section(reports['preprocessing']))
    
    # Duplicates section
    if 'duplicates' in reports:
        lines.extend(_generate_duplicates_section(reports['duplicates']))
    
    # Missing Values section
    if 'missing_values' in reports:
        lines.extend(_generate_missing_values_section(reports['missing_values']))
    
    # DateTime section
    if 'datetime' in reports:
        lines.extend(_generate_datetime_section(reports['datetime']))
    
    # Outliers section
    if 'outliers' in reports:
        lines.extend(_generate_outliers_section(reports['outliers']))
    
    # Structural Errors section
    if 'structural_errors' in reports:
        lines.extend(_generate_structural_errors_section(reports['structural_errors']))
    
    # Postprocessing section
    if 'postprocessing' in reports:
        lines.extend(_generate_postprocessing_section(reports['postprocessing']))
    
    # Write to file
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"Report saved: {filepath}")


# ============================================================================
# Section Generators (Private)
# ============================================================================

def _generate_summary(reports: dict) -> list:
    """Generate summary section."""
    lines = []
    lines.append("---")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    
    # Get shape info from preprocessing if available
    if 'preprocessing' in reports:
        r = reports['preprocessing']
        if 'original_shape' in r and r['original_shape']:
            lines.append(f"- **Original shape:** {r['original_shape'][0]} rows × {r['original_shape'][1]} columns")
        if 'final_shape' in r and r['final_shape']:
            lines.append(f"- **After preprocessing:** {r['final_shape'][0]} rows × {r['final_shape'][1]} columns")
    
    # Count total changes
    total_rows_deleted = 0
    total_imputations = 0
    total_outliers = 0
    total_values_changed = 0
    
    if 'duplicates' in reports:
        total_rows_deleted += reports['duplicates'].get('rows_removed', 0)
    
    if 'missing_values' in reports:
        total_rows_deleted += reports['missing_values'].get('rows_deleted', 0)
        total_imputations += len(reports['missing_values'].get('imputations', []))
    
    if 'datetime' in reports:
        total_rows_deleted += len(reports['datetime'].get('rows_deleted', []))
    
    if 'outliers' in reports:
        total_rows_deleted += reports['outliers'].get('rows_deleted', 0)
        total_outliers = reports['outliers'].get('total_outliers', 0)
    
    if 'structural_errors' in reports:
        # Handle both single report (dict) and multiple reports (list)
        struct_reports = reports['structural_errors']
        if isinstance(struct_reports, list):
            for r in struct_reports:
                total_values_changed += r.get('values_changed', 0)
        else:
            total_values_changed += struct_reports.get('values_changed', 0)
    
    if total_rows_deleted > 0:
        lines.append(f"- **Total rows deleted:** {total_rows_deleted}")
    if total_imputations > 0:
        lines.append(f"- **Total values imputed:** {total_imputations}")
    if total_outliers > 0:
        lines.append(f"- **Total outliers handled:** {total_outliers}")
    if total_values_changed > 0:
        lines.append(f"- **Total structural errors fixed:** {total_values_changed}")
    
    lines.append("")
    return lines


def _generate_preprocessing_section(report: dict) -> list:
    """Generate preprocessing section."""
    lines = []
    lines.append("---")
    lines.append("")
    lines.append("## Preprocessing")
    lines.append("")
    
    if report.get('rows_removed', 0) > 0:
        lines.append(f"- **Empty rows removed:** {report['rows_removed']}")
    if report.get('cols_removed', 0) > 0:
        lines.append(f"- **Empty columns removed:** {report['cols_removed']}")
    
    renamed = report.get('columns_renamed', [])
    if renamed:
        lines.append(f"- **Columns renamed:** {len(renamed)}")
        lines.append("")
        lines.append("| Original | New |")
        lines.append("|----------|-----|")
        for item in renamed[:10]:  # Show max 10
            lines.append(f"| {item['old']} | {item['new']} |")
        if len(renamed) > 10:
            lines.append(f"| ... | ({len(renamed) - 10} more) |")
    
    lines.append("")
    return lines


def _generate_duplicates_section(report: dict) -> list:
    """Generate duplicates section."""
    lines = []
    lines.append("---")
    lines.append("")
    lines.append("## Duplicates")
    lines.append("")
    
    rows = report.get('rows_removed', 0)
    cols = report.get('cols_removed', 0)
    
    if rows == 0 and cols == 0:
        lines.append("No duplicates found.")
    else:
        if rows > 0:
            lines.append(f"- **Duplicate rows removed:** {rows}")
        if cols > 0:
            lines.append(f"- **Duplicate columns removed:** {cols}")
    
    lines.append("")
    return lines


def _generate_missing_values_section(report: dict) -> list:
    """Generate missing values section."""
    lines = []
    lines.append("---")
    lines.append("")
    lines.append("## Missing Values")
    lines.append("")
    
    num_before = report.get('num_missing_before', 0)
    categ_before = report.get('categ_missing_before', 0)
    
    if num_before == 0 and categ_before == 0:
        lines.append("No missing values found.")
        lines.append("")
        return lines
    
    lines.append(f"- **Numerical missing:** {num_before}")
    lines.append(f"- **Categorical missing:** {categ_before}")
    lines.append(f"- **Method (numerical):** {report.get('method_num', 'N/A')}")
    lines.append(f"- **Method (categorical):** {report.get('method_categ', 'N/A')}")
    
    if report.get('rows_deleted', 0) > 0:
        lines.append(f"- **Rows deleted:** {report['rows_deleted']}")
    
    imputations = report.get('imputations', [])
    if imputations:
        lines.append("")
        lines.append("### Imputations")
        lines.append("")
        lines.append("| Row | Column | New Value | Method |")
        lines.append("|-----|--------|-----------|--------|")
        for imp in imputations[:20]:  # Show max 20
            val = imp['new_value']
            if isinstance(val, float):
                val = f"{val:.4g}"  # Compact float formatting
            lines.append(f"| {imp['row']} | {imp['column']} | {val} | {imp['method']} |")
        if len(imputations) > 20:
            lines.append(f"| ... | ... | ... | ({len(imputations) - 20} more) |")
    
    lines.append("")
    return lines


def _generate_datetime_section(report: dict) -> list:
    """Generate datetime standardization section."""
    lines = []
    lines.append("---")
    lines.append("")
    lines.append("## DateTime Standardization")
    lines.append("")
    
    lines.append(f"- **Column:** {report.get('column', 'N/A')}")
    lines.append(f"- **Format:** {report.get('format', 'N/A')}")
    lines.append(f"- **Invalid handling:** {report.get('handle_invalid', 'N/A')}")
    lines.append(f"- **Total values:** {report.get('total', 0)}")
    lines.append(f"- **Successfully converted:** {report.get('converted', 0)}")
    lines.append(f"- **Invalid:** {report.get('invalid', 0)}")
    
    rows_deleted = report.get('rows_deleted', [])
    if rows_deleted:
        lines.append(f"- **Rows deleted:** {len(rows_deleted)}")
    
    issues = report.get('issues', [])
    if issues:
        lines.append("")
        lines.append("### Issues Handled")
        lines.append("")
        lines.append("| Row | Original | Action |")
        lines.append("|-----|----------|--------|")
        for issue in issues[:20]:  # Show max 20
            lines.append(f"| {issue['row']} | {issue['original']} | {issue['action']} |")
        if len(issues) > 20:
            lines.append(f"| ... | ... | ... | ({len(issues) - 20} more) |")
    
    lines.append("")
    return lines


def _generate_outliers_section(report: dict) -> list:
    """Generate outliers section."""
    lines = []
    lines.append("---")
    lines.append("")
    lines.append("## Outliers")
    lines.append("")
    
    total = report.get('total_outliers', 0)
    
    if total == 0:
        lines.append("No outliers found.")
        lines.append("")
        return lines
    
    lines.append(f"- **Method:** {report.get('method', 'N/A')}")
    lines.append(f"- **Multiplier:** {report.get('multiplier', 1.5)}")
    lines.append(f"- **Total outliers:** {total}")
    
    if report.get('rows_deleted', 0) > 0:
        lines.append(f"- **Rows deleted:** {report['rows_deleted']}")
    
    outliers = report.get('outliers', [])
    if outliers:
        lines.append("")
        lines.append("### Outliers Handled")
        lines.append("")
        lines.append("| Row | Column | Original | New Value | Bound |")
        lines.append("|-----|--------|----------|-----------|-------|")
        for o in outliers[:20]:  # Show max 20
            orig = f"{o['original_value']:.4g}" if isinstance(o['original_value'], float) else o['original_value']
            new = f"{o['new_value']:.4g}" if isinstance(o['new_value'], float) else o['new_value']
            lines.append(f"| {o['row']} | {o['column']} | {orig} | {new} | {o['bound']} |")
        if len(outliers) > 20:
            lines.append(f"| ... | ... | ... | ... | ({len(outliers) - 20} more) |")
    
    lines.append("")
    return lines


def _generate_structural_errors_section(reports_input) -> list:
    """Generate structural errors section. Handles both single report (dict) and multiple reports (list)."""
    lines = []
    lines.append("---")
    lines.append("")
    lines.append("## Structural Errors")
    lines.append("")
    
    # Convert single report to list for uniform handling
    if isinstance(reports_input, dict):
        reports_list = [reports_input]
    else:
        reports_list = reports_input
    
    # Calculate totals across all reports
    total_values_changed = sum(r.get('values_changed', 0) for r in reports_list)
    total_columns = len(reports_list)
    
    lines.append(f"- **Columns processed:** {total_columns}")
    lines.append(f"- **Total values changed:** {total_values_changed}")
    lines.append("")
    
    # Generate section for each column
    for i, report in enumerate(reports_list):
        column_name = report.get('column', f'Column {i+1}')
        lines.append(f"### {column_name}")
        lines.append("")
        
        lines.append(f"- **Similarity method:** {report.get('similarity', 'N/A')}")
        lines.append(f"- **Clustering method:** {report.get('clustering', 'N/A')}")
        lines.append(f"- **Canonical selection:** {report.get('canonical', 'N/A')}")
        
        # Show relevant threshold based on clustering method
        clustering = report.get('clustering', '')
        if clustering == 'hierarchical':
            lines.append(f"- **Threshold:** {report.get('threshold_h', 0.85)}")
        elif clustering == 'connected_components':
            lines.append(f"- **Threshold:** {report.get('threshold_cc', 0.85)}")
        # affinity_propagation has no threshold
        
        # Show embedding model if embeddings were used
        if report.get('similarity') == 'embeddings':
            lines.append(f"- **Embedding model:** {report.get('embedding_model', 'N/A')}")
        
        lines.append(f"- **Unique values before:** {report.get('unique_values_before', 'N/A')}")
        lines.append(f"- **Unique values after:** {report.get('unique_values_after', 'N/A')}")
        lines.append(f"- **Values changed:** {report.get('values_changed', 0)}")
        
        # Show mapping
        mapping = report.get('mapping', {})
        value_counts = report.get('value_counts', {})
        
        if mapping:
            # Group by canonical value to show clusters
            clusters = {}
            for original, canonical in mapping.items():
                if canonical not in clusters:
                    clusters[canonical] = []
                clusters[canonical].append(original)
            
            # Table 1: Clustering results
            lines.append("")
            lines.append("#### Clustering Results")
            lines.append("")
            lines.append("| Original Values | Canonical |")
            lines.append("|-----------------|-----------|")
            
            # Sort clusters by total count (descending)
            sorted_clusters = sorted(clusters.items(), 
                                    key=lambda x: sum(value_counts.get(orig, 0) for orig in x[1]), 
                                    reverse=True)
            
            for canonical, originals in sorted_clusters:
                originals_str = "; ".join(originals)
                lines.append(f"| {originals_str} | {canonical} |")
        
        # Table 2: Value counts (from original data)
        '''
        if value_counts:
            lines.append("")
            lines.append("#### Value Counts (Original Data)")
            lines.append("")
            lines.append("| Value | Count |")
            lines.append("|-------|-------|")
            
            # Sort by count descending
            sorted_counts = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
            
            for value, count in sorted_counts:
                lines.append(f"| {value} | {count} |")
        '''
        lines.append("")

    return lines


def _generate_postprocessing_section(report: dict) -> list:
    """Generate postprocessing section."""
    lines = []
    lines.append("---")
    lines.append("")
    lines.append("## Postprocessing")
    lines.append("")
    
    changes = report.get('changes', [])
    if changes:
        lines.append("| Column | Action |")
        lines.append("|--------|--------|")
        for c in changes:
            lines.append(f"| {c['column']} | {c['action']} |")
    else:
        lines.append("No postprocessing changes applied.")
    
    lines.append("")
    return lines