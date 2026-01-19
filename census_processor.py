import pandas as pd
from pathlib import Path

print("=" * 80)
print("CENSUS 2011 – AUTO PROCESSOR (RAW or CLEAN)")
print("=" * 80)

# =============================================================================
# PATH SETUP (ABSOLUTE & SAFE)
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent
EXTERNAL_PATH = PROJECT_ROOT / "data" / "external"
EXTERNAL_PATH.mkdir(parents=True, exist_ok=True)

INPUT_FILE = EXTERNAL_PATH / "census_2011_district_population.csv"
OUTPUT_FILE = EXTERNAL_PATH / "census_2011_district_population_clean.csv"

print(f"\n📂 Project root: {PROJECT_ROOT}")
print(f"📂 External folder: {EXTERNAL_PATH}")
print(f"📄 Input file: {INPUT_FILE}")

if not INPUT_FILE.exists():
    raise FileNotFoundError(f"❌ Input file not found: {INPUT_FILE}")

# =============================================================================
# STEP 1: LOAD DATA
# =============================================================================

df = pd.read_csv(INPUT_FILE)
print(f"\n✅ File loaded: {df.shape}")
print("📋 Columns:", df.columns.tolist())

# =============================================================================
# STEP 2: DETECT FILE TYPE
# =============================================================================

is_clean = {"state", "district", "population_2011", "population_2025"}.issubset(df.columns)
is_raw = {"Level", "TRU", "Name", "TOT_P", "State"}.issubset(df.columns)

# =============================================================================
# STEP 3A: IF CLEAN → JUST VERIFY
# =============================================================================

if is_clean:
    print("\n🟢 Detected CLEAN census file")

    census_clean = df.copy()

# =============================================================================
# STEP 3B: IF RAW → PROCESS IT
# =============================================================================

elif is_raw:
    print("\n🟡 Detected RAW Census PCA file — processing...")

    # Filter DISTRICT + Total population
    census_clean = df[
        (df["Level"] == "DISTRICT") &
        (df["TRU"] == "Total")
    ].copy()

    # Rename key columns
    census_clean = census_clean.rename(columns={
        "Name": "district",
        "TOT_P": "population_2011"
    })

    # Map state codes → state names
    state_map = df[
        (df["Level"] == "STATE") &
        (df["TRU"] == "Total")
    ][["State", "Name"]].drop_duplicates()

    state_map = state_map.rename(columns={"Name": "state"})

    census_clean = census_clean.merge(
        state_map,
        on="State",
        how="left"
    )

    # Clean text
    census_clean["state"] = census_clean["state"].str.strip().str.title()
    census_clean["district"] = census_clean["district"].str.strip().str.title()

    census_clean = census_clean[["state", "district", "population_2011"]]
    census_clean = census_clean.drop_duplicates()

    # Project to 2025
    ANNUAL_GROWTH_RATE = 0.012
    YEARS_ELAPSED = 2025 - 2011

    census_clean["population_2025"] = (
        census_clean["population_2011"]
        * (1 + ANNUAL_GROWTH_RATE) ** YEARS_ELAPSED
    ).round(0).astype(int)

else:
    raise ValueError("❌ Unknown file format. Cannot process.")

# =============================================================================
# STEP 4: FINAL VALIDATION
# =============================================================================

required_cols = {"state", "district", "population_2011", "population_2025"}
missing = required_cols - set(census_clean.columns)

if missing:
    raise ValueError(f"❌ Still missing columns after processing: {missing}")

print("\n✅ Final dataset validated")
print(f"   Districts: {len(census_clean)}")
print(f"   States/UTs: {census_clean['state'].nunique()}")
print(f"   Population 2011: {census_clean['population_2011'].sum():,}")
print(f"   Population 2025: {census_clean['population_2025'].sum():,}")

# =============================================================================
# STEP 5: SAVE CLEAN DATA
# =============================================================================

census_clean.to_csv(OUTPUT_FILE, index=False)

print(f"\n💾 Clean census file saved to:")
print(f"   {OUTPUT_FILE.resolve()}")

print("\n📋 Sample rows:")
print(census_clean.head(10).to_string(index=False))

print("\n" + "=" * 80)
print("✨ CENSUS PROCESSING COMPLETED SUCCESSFULLY")
print("=" * 80)
