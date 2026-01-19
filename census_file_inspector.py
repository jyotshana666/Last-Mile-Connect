import pandas as pd
from pathlib import Path

print("="*80)
print("CENSUS 2011 FILE INSPECTION")
print("="*80)

# Try to load the Excel file
file_path = "C:\Work\Projects\Last-mile-connect\data\external\census_2011_district_population.csv"

try:
    # Read Excel file (try first sheet)
    df = pd.read_csv(file_path)
    
    print(f"\n✅ File loaded successfully!")
    print(f"\n📊 File Information:")
    print(f"   Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    print(f"\n📋 Column Names:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2d}. {col}")
    
    print(f"\n👀 First 10 rows:")
    print(df.head(10))
    
    print(f"\n📈 Data Types:")
    print(df.dtypes)
    
    # Check for key columns we need
    print(f"\n🔍 Checking for Required Columns:")
    required_keywords = ['state', 'district', 'population', 'total']
    
    found_cols = {}
    for keyword in required_keywords:
        matching = [col for col in df.columns if keyword.lower() in str(col).lower()]
        if matching:
            found_cols[keyword] = matching
            print(f"   ✅ '{keyword}' related columns: {matching}")
        else:
            print(f"   ⚠️  No '{keyword}' column found")
    
    # Check if this looks like district-level data
    print(f"\n🗺️  Geographic Coverage Check:")
    
    # Try to identify state/district columns
    potential_state_cols = [col for col in df.columns if 'state' in str(col).lower()]
    potential_district_cols = [col for col in df.columns if 'district' in str(col).lower()]
    
    if potential_state_cols:
        state_col = potential_state_cols[0]
        print(f"   Unique states/UTs: {df[state_col].nunique()}")
        print(f"   Sample states: {df[state_col].unique()[:5].tolist()}")
    
    if potential_district_cols:
        district_col = potential_district_cols[0]
        print(f"   Unique districts: {df[district_col].nunique()}")
        print(f"   Sample districts: {df[district_col].unique()[:5].tolist()}")
    
    # Check for population data
    potential_pop_cols = [col for col in df.columns 
                          if any(keyword in str(col).lower() 
                          for keyword in ['population', 'total', 'persons'])]
    
    if potential_pop_cols:
        print(f"\n📊 Population Data Columns:")
        for col in potential_pop_cols[:5]:  # Show first 5
            print(f"   - {col}")
            if pd.api.types.is_numeric_dtype(df[col]):
                print(f"     Range: {df[col].min():,} to {df[col].max():,}")
    
    # Final verdict
    print(f"\n" + "="*80)
    print("📝 VERDICT:")
    print("="*80)
    
    has_state = len(potential_state_cols) > 0
    has_district = len(potential_district_cols) > 0
    has_population = len(potential_pop_cols) > 0
    
    if has_state and has_district and has_population:
        print("✅ YES! This appears to be Census 2011 district-level data!")
        print(f"\n🎯 Recommended columns to use:")
        if potential_state_cols:
            print(f"   State column: '{potential_state_cols[0]}'")
        if potential_district_cols:
            print(f"   District column: '{potential_district_cols[0]}'")
        if potential_pop_cols:
            print(f"   Population column: '{potential_pop_cols[0]}'")
    else:
        print("⚠️  This file may not have all required columns.")
        print(f"   Has state data: {'✅' if has_state else '❌'}")
        print(f"   Has district data: {'✅' if has_district else '❌'}")
        print(f"   Has population data: {'✅' if has_population else '❌'}")
    
except Exception as e:
    print(f"\n❌ Error loading file: {e}")
    print(f"\nTroubleshooting:")
    print(f"   1. Make sure the file is in the current directory")
    print(f"   2. Check if you have openpyxl installed: pip install openpyxl")
    print(f"   3. Try opening in Excel to verify it's not corrupted")

print("\n" + "="*80)

