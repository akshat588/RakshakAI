import pandas as pd

from config.paths import URL_DATASET

dataset_path = URL_DATASET / "urls.csv"

df = pd.read_csv(dataset_path)

print("=" * 60)
print("URL DATASET INFORMATION")
print("=" * 60)

print("\nFirst 5 Rows:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print("\nShape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nLabel Distribution:")
print(df["status"].value_counts())
