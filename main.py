#!/usr/bin/env python3
"""
Main script demonstrating LLM-powered data cleaning.

Usage:
    export OPENAI_API_KEY="sk-..."
    python main.py
"""

import os
import json
from Functions.Structural_Errors import LLMDataCleaner


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: Set OPENAI_API_KEY environment variable")
        return
    
    cleaner = LLMDataCleaner(api_key=api_key)
    
    # ==========================================================================
    # Example 1: City Names
    # ==========================================================================
    print("\n" + "="*70)
    print(" EXAMPLE 1: City Names")
    print("="*70)
    
    cities = [
        "New York", "new york", "NY", "New Yrok", "NYC", "N.Y.",
        "Boston", "boston", "BOSTON", "Bsoton",
        "Los Angeles", "los angeles", "LA", "L.A.", "Los Angles",
    ]
    
    print("\nInput:")
    for city in cities:
        print(f"  • '{city}'")
    
    result = cleaner.clean(cities)
    
    print("\n" + "-"*50)
    print("OUTPUT MAPPING:")
    print(json.dumps(result.mappings, indent=2))
    
    print("\nCLUSTER DETAILS:")
    for c in result.clusters:
        print(f"  {c.members} → '{c.canonical_form}' ({c.confidence:.0%})")
    
    # ==========================================================================
    # Example 2: Company Names
    # ==========================================================================
    print("\n" + "="*70)
    print(" EXAMPLE 2: Company Names")
    print("="*70)
    
    companies = [
        "Apple Inc.", "Apple", "APPLE INC", "apple inc",
        "Microsoft", "Microsoft Corporation", "MSFT", "microsoft corp",
        "Google", "google", "Google LLC", "GOOGLE",
    ]
    
    print("\nInput:")
    for company in companies:
        print(f"  • '{company}'")
    
    result = cleaner.clean(companies)
    
    print("\n" + "-"*50)
    print("OUTPUT MAPPING:")
    print(json.dumps(result.mappings, indent=2))
    
    # ==========================================================================
    # Example 3: Product Names
    # ==========================================================================
    print("\n" + "="*70)
    print(" EXAMPLE 3: Product Names")
    print("="*70)
    
    products = [
        "iPhone 15 Pro", "iphone 15 pro", "iPhone15Pro", "IPHONE 15 PRO",
        "MacBook Pro", "macbook pro", "Macbook Pro", "MBP",
        "AirPods Pro", "airpods pro", "Air Pods Pro",
    ]
    
    print("\nInput:")
    for product in products:
        print(f"  • '{product}'")
    
    result = cleaner.clean(products)
    
    print("\n" + "-"*50)
    print("OUTPUT MAPPING:")
    print(json.dumps(result.mappings, indent=2))
    
    print("\nSTATISTICS:")
    print(f"  Input count:    {result.stats['input_count']}")
    print(f"  Unique values:  {result.stats['unique_count']}")
    print(f"  Clusters found: {result.stats['cluster_count']}")


if __name__ == "__main__":
    main()