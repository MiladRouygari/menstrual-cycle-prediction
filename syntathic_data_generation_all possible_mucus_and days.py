import pandas as pd

# Define cycle length and mucus types
cycle_length = 28
# Define Mucus
mucus_types = ['none', 'sticky', 'creamy', 'egg white', 'watery']

# Generate the rows: each day has all mucus types
output_rows = []
for day in range(1, cycle_length + 1):  # Day 1 to Day 28
    for mucus in mucus_types:
        output_rows.append({
            'day': day,
            'today_mucus': mucus
        })

# Create DataFrame and export
df = pd.DataFrame(output_rows)
file_name = f'csv_files/day_mucus_combinations_cycle_length_{cycle_length}.csv'
df.to_csv(file_name, index=False)

print(f"CSV file '{file_name}' created successfully.")

