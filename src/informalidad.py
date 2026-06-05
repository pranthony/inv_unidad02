import pandas as pd

df = pd.read_csv(
    "data/raw/Enaho01a-2025-500.csv",
    sep=";",
    encoding="latin1",
    low_memory=False
)

print(df.columns.tolist())