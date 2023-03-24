# Importing pandas package
import pandas as pd

# Create DataFrame
df = pd.read_csv("experiment_details.csv")

df.sort_values(['Instance', 'BS', 'ExecutionTime'], axis=0, ascending=True, inplace=True)

df['Gap'] = df['Gap'].round(2)

df['ExecutionTime'] = df['ExecutionTime'].round(2)

# Groupby function
result = df.groupby('Instance', as_index=False)

# Selecting 1st row of group by result
final = result.nth(0)

print(
	final['BS'].mean(), end="\t"
)
print(
	final['Gap'].mean(), end="\t"
)
print(
	final['ExecutionTime'].mean(), end="\t"
)

# Export to CSV file
final.to_csv('experiment_best.csv', index=False)

