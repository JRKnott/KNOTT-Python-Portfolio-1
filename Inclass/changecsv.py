import pandas as pd

# Load the CSV and parse the 'Date' column as datetime
df = pd.read_csv("FinalProj/joined_closesmost_popular.csv", parse_dates=["Date"])

# Optionally set 'Date' as the index if you plan to work with time series
df.set_index("Date", inplace=True)

# Save back to CSV if you want to permanently store it with proper datetime format
df.to_csv("FinalProj/joined_closesmost_popular.csv")

print(df.index.dtype)