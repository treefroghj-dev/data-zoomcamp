import pandas as pd
import sys

month = sys.argv[1]
df = pd.DataFrame({"A":[1,2], "B":[3,4]})
df["month"] = month

print(df.head())