"""
LLM Data Cleaning - Test Suite

Easy and difficult clustering examples to test the cleaner.

Usage:
    export OPENAI_API_KEY="sk-..."
    python main.py
"""

import os
import json
from Functions.Structural_Errors import LLMDataCleaner


# =============================================================================
# EASY EXAMPLES
# =============================================================================

cities = [
    # New York (6)
    "New York", "new york", "NY", "NYC", "New Yrok", "N.Y.",
    # Boston (4)
    "Boston", "boston", "BOSTON", "Bsoton",
    # Los Angeles (5)
    "Los Angeles", "los angeles", "LA", "L.A.", "Los Angles",
]
# Expected: 3 clusters

countries = [
    # United States (6)
    "United States", "USA", "U.S.A.", "United States of America", "US", "united states",
    # United Kingdom (5)
    "United Kingdom", "UK", "U.K.", "Great Britain", "united kingdom",
    # Germany (4)
    "Germany", "GERMANY", "germany", "Deutschland",
]
# Expected: 3 clusters

colors = [
    # Red (4)
    "Red", "red", "RED", "Redd",
    # Blue (4)
    "Blue", "blue", "BLUE", "Bleu",
    # Green (4)
    "Green", "green", "GREEN", "Grren",
]
# Expected: 3 clusters


# =============================================================================
# MEDIUM EXAMPLES
# =============================================================================

companies = [
    # Apple (5)
    "Apple Inc.", "Apple", "APPLE INC", "apple inc", "Apple, Inc.",
    # Microsoft (5)
    "Microsoft", "Microsoft Corporation", "MSFT", "microsoft corp", "Microsoft Corp.",
    # Google (5)
    "Google", "google", "Google LLC", "GOOGLE", "Alphabet",
    # Amazon (4)
    "Amazon", "Amazon.com", "AMZN", "amazon",
]
# Expected: 4 clusters

job_titles = [
    # Software Engineer (5)
    "Software Engineer", "software engineer", "Software Dev", "SW Engineer", "Software Developer",
    # Data Scientist (5)
    "Data Scientist", "data scientist", "Data Science", "Data Analyst", "DATA SCIENTIST",
    # Product Manager (5)
    "Product Manager", "product manager", "PM", "Product Mgr", "Prodcut Manager",
    # Project Manager (SIMILAR to Product Manager!) (4)
    "Project Manager", "project manager", "Proj Manager", "Project Mgr",
]
# Expected: 4 clusters


# =============================================================================
# DIFFICULT EXAMPLES
# =============================================================================

medical_conditions = [
    # === Type 2 Diabetes Mellitus (8) ===
    "Type 2 Diabetes Mellitus",
    "Diabetes Mellitus Type 2",
    "T2DM",
    "Type II Diabetes",
    "Diabetes Type 2",
    "Type 2 Diabetes",
    "DM Type 2",
    "type 2 diabetes mellitus",
    
    # === Type 1 Diabetes Mellitus - VERY SIMILAR! (8) ===
    "Type 1 Diabetes Mellitus",
    "Diabetes Mellitus Type 1",
    "T1DM",
    "Type I Diabetes",
    "Diabetes Type 1",
    "Type 1 Diabetes",
    "DM Type 1",
    "Juvenile Diabetes",
    
    # === Chronic Obstructive Pulmonary Disease (6) ===
    "Chronic Obstructive Pulmonary Disease",
    "COPD",
    "Chronic Obstructive Lung Disease",
    "Obstructive Pulmonary Disease, Chronic",
    "Chr. Obstructive Pulmonary Dis.",
    "chronic obstructive pulmonary disease",
    
    # === Chronic Kidney Disease Stage 4 (7) ===
    "Stage 4 Chronic Kidney Disease",
    "CKD Stage 4",
    "Chronic Kidney Disease Stage IV",
    "Stage IV CKD",
    "CKD-4",
    "Chronic Kidney Disease, Stage 4",
    "stage 4 ckd",
    
    # === Chronic Kidney Disease Stage 3 - VERY SIMILAR! (7) ===
    "Stage 3 Chronic Kidney Disease",
    "CKD Stage 3",
    "Chronic Kidney Disease Stage III",
    "Stage III CKD",
    "CKD-3",
    "Chronic Kidney Disease, Stage 3",
    "stage 3 ckd",
    
    # === Acute Myocardial Infarction (7) ===
    "Acute Myocardial Infarction",
    "AMI",
    "Myocardial Infarction, Acute",
    "Heart Attack",
    "Acute MI",
    "Myocardial Infarction (Acute)",
    "acute myocardial infarction",
    
    # === Acute Kidney Injury - SIMILAR pattern! (7) ===
    "Acute Kidney Injury",
    "AKI",
    "Acute Renal Failure",
    "Kidney Injury, Acute",
    "Acute Renal Injury",
    "acute kidney injury",
    "ARF",
    
    # === Rheumatoid Arthritis (5) ===
    "Rheumatoid Arthritis",
    "RA",
    "Rheumatoid Arthitis",
    "rheumatoid arthritis",
    "Arthritis, Rheumatoid",
    
    # === Osteoarthritis - SIMILAR! (6) ===
    "Osteoarthritis",
    "OA",
    "Degenerative Arthritis",
    "osteoarthritis",
    "Arthritis, Osteo",
    "Degenerative Joint Disease",
    
    # === Non-Small Cell Lung Cancer (6) ===
    "Non-Small Cell Lung Cancer",
    "NSCLC",
    "Non Small Cell Lung Cancer",
    "Lung Cancer, Non-Small Cell",
    "Non-Small Cell Lung Carcinoma",
    "nsclc",
    
    # === Small Cell Lung Cancer - VERY SIMILAR! (6) ===
    "Small Cell Lung Cancer",
    "SCLC",
    "Small Cell Lung Carcinoma",
    "Lung Cancer, Small Cell",
    "sclc",
    "Oat Cell Carcinoma",
]
# Expected: 11 clusters


product_categories = [
    # === iPhone 15 Pro (6) ===
    "iPhone 15 Pro",
    "iphone 15 pro",
    "IPHONE 15 PRO",
    "iPhone15Pro",
    "Apple iPhone 15 Pro",
    "iPhone 15-Pro",
    
    # === iPhone 15 - VERY SIMILAR! (5) ===
    "iPhone 15",
    "iphone 15",
    "IPHONE 15",
    "iPhone15",
    "Apple iPhone 15",
    
    # === iPhone 14 Pro - SIMILAR! (5) ===
    "iPhone 14 Pro",
    "iphone 14 pro",
    "iPhone14Pro",
    "Apple iPhone 14 Pro",
    "IPHONE 14 PRO",
    
    # === Samsung Galaxy S24 (5) ===
    "Samsung Galaxy S24",
    "Galaxy S24",
    "samsung galaxy s24",
    "SAMSUNG GALAXY S24",
    "Samsung S24",
    
    # === Samsung Galaxy S24 Ultra - SIMILAR! (5) ===
    "Samsung Galaxy S24 Ultra",
    "Galaxy S24 Ultra",
    "samsung galaxy s24 ultra",
    "Samsung S24 Ultra",
    "S24 Ultra",
    
    # === MacBook Pro 14 (5) ===
    "MacBook Pro 14",
    "macbook pro 14",
    "MacBook Pro 14-inch",
    "MBP 14",
    "Apple MacBook Pro 14",
    
    # === MacBook Pro 16 - SIMILAR! (5) ===
    "MacBook Pro 16",
    "macbook pro 16",
    "MacBook Pro 16-inch",
    "MBP 16",
    "Apple MacBook Pro 16",
]
# Expected: 7 clusters


# =============================================================================
# TEST RUNNER
# =============================================================================

def run_test(cleaner, name, data, expected_clusters, difficulty):
    """Run a single test."""
    print(f"\n{'='*70}")
    print(f" [{difficulty}] {name}")
    print(f" Items: {len(data)} | Expected clusters: {expected_clusters}")
    print(f"{'='*70}")
    
    print("\nInput:")
    for i, item in enumerate(data, 1):
        print(f"  {i:2}. '{item}'")
    
    result = cleaner.clean(data)
    
    print("\n" + "-"*50)
    print(f"CLUSTERS FOUND: {result.stats['cluster_count']}")
    print("-"*50)
    
    for c in result.clusters:
        print(f"\n  → '{c.canonical_form}' ({len(c.members)} items)")
        for m in c.members:
            print(f"      - '{m}'")
    
    # Evaluation
    status = "✓ PASS" if result.stats['cluster_count'] == expected_clusters else "✗ FAIL"
    print(f"\n{status}: Expected {expected_clusters}, Got {result.stats['cluster_count']}")
    
    return {
        "name": name,
        "difficulty": difficulty,
        "expected": expected_clusters,
        "actual": result.stats['cluster_count'],
        "passed": result.stats['cluster_count'] == expected_clusters
    }


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: Set OPENAI_API_KEY environment variable")
        print("  export OPENAI_API_KEY='sk-...'")
        return
    
    cleaner = LLMDataCleaner(api_key=api_key, verbose=True)
    
    results = []
    
    # === EASY TESTS ===
    results.append(run_test(cleaner, "Cities", cities, 3, "EASY"))
    results.append(run_test(cleaner, "Countries", countries, 3, "EASY"))
    results.append(run_test(cleaner, "Colors", colors, 3, "EASY"))
    
    # === MEDIUM TESTS ===
    results.append(run_test(cleaner, "Companies", companies, 4, "MEDIUM"))
    results.append(run_test(cleaner, "Job Titles", job_titles, 4, "MEDIUM"))
    
    # === DIFFICULT TESTS ===
    results.append(run_test(cleaner, "Medical Conditions", medical_conditions, 11, "HARD"))
    results.append(run_test(cleaner, "Product Categories", product_categories, 7, "HARD"))
    
    # === SUMMARY ===
    print("\n" + "="*70)
    print(" SUMMARY")
    print("="*70)
    
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    
    for r in results:
        status = "✓" if r["passed"] else "✗"
        print(f"  {status} [{r['difficulty']:6}] {r['name']:25} "
              f"Expected: {r['expected']:2} | Got: {r['actual']:2}")
    
    print(f"\n  Total: {passed}/{total} passed")
    
    if passed == total:
        print("\n  🎉 All tests passed!")
    else:
        print(f"\n  ⚠️  {total - passed} test(s) failed")


if __name__ == "__main__":
    main()