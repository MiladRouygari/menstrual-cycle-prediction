import pandas as pd


def generate_day_mucus_combinations(cycle_length=28):
    """
    Generate all possible combinations of days and mucus types for a menstrual cycle.
    
    Args:
        cycle_length (int): Length of the menstrual cycle in days. Default is 28.
        
    Returns:
        pd.DataFrame: DataFrame containing all combinations of days and mucus types.
    """
    # Define mucus types
    mucus_types = ['none', 'sticky', 'creamy', 'egg white', 'watery']

    # Generate the rows: each day has all mucus types
    output_rows = []
    for day in range(1, cycle_length + 1):  # Day 1 to End of Cycle
        for mucus in mucus_types:
            output_rows.append({
                'day': day,
                'today_mucus': mucus
            })

    # Create DataFrame and export
    df = pd.DataFrame(output_rows)
    file_name = f'csv_files/day_mucus_combinations_cycle_length_{cycle_length}.csv'
    df.to_csv(file_name, index=False)
    
    return df

generate_day_mucus_combinations(cycle_length=28)  # You can change the cycle length as needed
