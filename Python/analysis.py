# ============================================================
# ROAD ACCIDENT DATA ANALYSIS PROJECT
# Technologies: Python, Pandas, Matplotlib
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Configure project directories
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 65)
print("ROAD ACCIDENT DATA ANALYSIS PROJECT")
print("=" * 65)

# 2. Locate the source dataset
possible_files = [
    BASE_DIR / "Indian_Road_Safety_RawData2023.csv",
    BASE_DIR / "Indian_Road_Safety_CleanedData.csv",
]

input_file = next(
    (file for file in possible_files if file.exists()),
    None
)

if input_file is None:
    print("\nError: The input dataset could not be found.")
    print("Please check the CSV filename and project directory.")
    raise SystemExit(1)

# 3. Load the dataset
df = pd.read_csv(input_file, encoding="utf-8-sig")

print(f"\nSource file: {input_file.name}")
print(f"Original row count: {len(df)}")
print(f"Original column count: {len(df.columns)}")

# 4. Standardize column names
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

# 5. Remove completely empty rows and columns
df = df.dropna(how="all")
df = df.dropna(axis=1, how="all")

# 6. Validate the location column
location_column = "State/Ut/"

if location_column not in df.columns:
    print("\nError: The required location column was not found.")
    print("Available columns:")
    print(df.columns.tolist())
    raise SystemExit(1)

# 7. Separate summary records from analytical records
summary_labels = [
    "Total (States)",
    "Total (UTs)",
    "Total (All India)",
    "Total (Cities)",
]

location_values = df[location_column].astype(str).str.strip()

summary_df = df[
    location_values.isin(summary_labels)
].copy()

analysis_df = df[
    ~location_values.isin(summary_labels)
].copy()

print(f"\nSummary records identified: {len(summary_df)}")
print(f"Records retained for analysis: {len(analysis_df)}")

# 8. Convert accident-related columns to numeric values
excluded_columns = [location_column, "Sr. No."]

numeric_candidate_columns = [
    column for column in analysis_df.columns
    if column not in excluded_columns
]

for column in numeric_candidate_columns:
    analysis_df[column] = pd.to_numeric(
        analysis_df[column]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip(),
        errors="coerce"
    )

# 9. Remove exact duplicate records
initial_count = len(analysis_df)

analysis_df = analysis_df.drop_duplicates()

duplicates_removed = initial_count - len(analysis_df)

print(f"Exact duplicate records removed: {duplicates_removed}")

# 10. Export cleaned data and summary records
cleaned_data_path = OUTPUT_DIR / "clean_road_accident_data.csv"
summary_data_path = OUTPUT_DIR / "summary_rows.csv"

analysis_df.to_csv(
    cleaned_data_path,
    index=False,
    encoding="utf-8-sig"
)

summary_df.to_csv(
    summary_data_path,
    index=False,
    encoding="utf-8-sig"
)

print("\nCleaned dataset exported successfully.")
print("Summary records exported successfully.")

# 11. Report missing values
print("\nMISSING VALUES BY COLUMN")
print(analysis_df.isnull().sum().to_string())

# 12. Generate descriptive statistics
numeric_columns = analysis_df.select_dtypes(
    include="number"
).columns

print("\nDESCRIPTIVE STATISTICS")
print(analysis_df[numeric_columns].describe().round(2))

# 13. Summarize accident metrics
metric_columns = [
    "Road Accidents - Cases",
    "Road Accidents - Injured",
    "Road Accidents - Died",
    "Railway Accidents - Cases",
    "Railway Accidents - Injured",
    "Railway Accidents - Died",
    "Railway Crossing Accidents - Cases",
    "Railway Crossing Accidents - Injured",
    "Railway Crossing Accidents - Died",
    "Total Traffic Accidents - Cases",
    "Total Traffic Accidents - Injured",
    "Total Traffic Accidents - Died",
]

available_metrics = [
    column for column in metric_columns
    if column in analysis_df.columns
]

print("\nAGGREGATED ACCIDENT METRICS")

for column in available_metrics:
    total_value = analysis_df[column].sum(skipna=True)
    print(f"{column}: {total_value:,.0f}")

# 14. Analyze the top 10 locations by accident cases
cases_column = "Total Traffic Accidents - Cases"

if cases_column in analysis_df.columns:
    top_cases = analysis_df.nlargest(10, cases_column)

    print("\nTOP 10 LOCATIONS BY TRAFFIC ACCIDENT CASES")
    print(
        top_cases[[location_column, cases_column]]
        .to_string(index=False)
    )

    plt.figure(figsize=(12, 6))
    plt.bar(
        top_cases[location_column].astype(str),
        top_cases[cases_column]
    )
    plt.title("Top 10 Locations by Traffic Accident Cases")
    plt.xlabel("Location")
    plt.ylabel("Number of Accident Cases")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "top_10_accident_cases.png",
        dpi=150
    )
    plt.close()

# 15. Analyze the top 10 locations by accident deaths
deaths_column = "Total Traffic Accidents - Died"

if deaths_column in analysis_df.columns:
    top_deaths = analysis_df.nlargest(10, deaths_column)

    print("\nTOP 10 LOCATIONS BY TRAFFIC ACCIDENT DEATHS")
    print(
        top_deaths[[location_column, deaths_column]]
        .to_string(index=False)
    )

    plt.figure(figsize=(12, 6))
    plt.bar(
        top_deaths[location_column].astype(str),
        top_deaths[deaths_column]
    )
    plt.title("Top 10 Locations by Traffic Accident Deaths")
    plt.xlabel("Location")
    plt.ylabel("Number of Deaths")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "top_10_accident_deaths.png",
        dpi=150
    )
    plt.close()

# 16. Compare accident cases by type
accident_type_columns = [
    "Road Accidents - Cases",
    "Railway Accidents - Cases",
    "Railway Crossing Accidents - Cases",
]

available_type_columns = [
    column for column in accident_type_columns
    if column in analysis_df.columns
]

if available_type_columns:
    type_totals = analysis_df[available_type_columns].sum()

    print("\nACCIDENT CASES BY TYPE")
    print(type_totals.to_string())

    plt.figure(figsize=(10, 5))
    plt.bar(type_totals.index, type_totals.values)
    plt.title("Comparison of Accident Cases by Type")
    plt.xlabel("Accident Type")
    plt.ylabel("Number of Cases")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "accident_types_comparison.png",
        dpi=150
    )
    plt.close()

# 17. Calculate correlations between accident metrics
correlation_columns = [
    column for column in [
        "Total Traffic Accidents - Cases",
        "Total Traffic Accidents - Injured",
        "Total Traffic Accidents - Died",
    ]
    if column in analysis_df.columns
]

if len(correlation_columns) >= 2:
    correlation_matrix = analysis_df[
        correlation_columns
    ].corr()

    print("\nCORRELATION MATRIX")
    print(correlation_matrix.round(2))

    plt.figure(figsize=(8, 6))
    plt.imshow(correlation_matrix, aspect="auto")
    plt.colorbar(label="Correlation Coefficient")
    plt.xticks(
        range(len(correlation_columns)),
        correlation_columns,
        rotation=35,
        ha="right"
    )
    plt.yticks(
        range(len(correlation_columns)),
        correlation_columns
    )
    plt.title("Correlation Between Accident Metrics")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "correlation_matrix.png",
        dpi=150
    )
    plt.close()

# 18. Export data for Power BI
power_bi_path = OUTPUT_DIR / "power_bi_import.csv"

analysis_df.to_csv(
    power_bi_path,
    index=False,
    encoding="utf-8-sig"
)

# 19. Display the completion summary
print("\n" + "=" * 65)
print("DATA ANALYSIS COMPLETED SUCCESSFULLY")
print(f"Output directory: {OUTPUT_DIR}")
print("Cleaned data has been exported.")
print("Summary records have been saved separately.")
print("Visualization charts have been generated where applicable.")
print("The Power BI import file is ready.")
print("=" * 65)