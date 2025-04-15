"""
TODO:
"""

from datetime import datetime, timedelta

now = datetime.now()
print(now)
# datetime original order is "%Y-%m-%d"


def is_valid_date(date:str):
    """
     Validates whether a given date string is in the 'YYYY-MM-DD' format.

    Parameters:
        date (str): The date string to validate.

    Returns:
        bool: True if the string is a valid date in 'YYYY-MM-DD' format.
    
    """
    
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        raise ValueError("current_cycle_start_str must be in 'YYYY-MM-DD' format")


def calculate_future_cycle_phases(current_cycle_start:str, cycle_length:int):
    """
        Calculates and prints the phases of the menstrual cycle based on the start date and cycle length.

    The function determines:
      - The next expected cycle start date
      - The ovulation day (assumed to be 14 days before the next cycle)
      - The follicular phase (from the current cycle start to the day before ovulation)
      - The luteal phase hard coded as 14 days (from ovulation to the day before the next cycle)

    Parameters:
        current_cycle_start (str): The start date of the current menstrual cycle, in 'YYYY-MM-DD' format.
        cycle_length (int): The total length of the cycle in days (must be between 21 and 35).
    
    Returns:
        print statemants determining the cycle phases (Follicular Phase, Ovulation Day, Luteal Phase)
    
    """

    # Checking inputs
    # Validate date format
    is_valid_date(current_cycle_start)
        
    # Validate cycle length 
    if not (21 <= cycle_length <= 35):
        raise ValueError("cycle_length must be between 21 and 35 days")


    # Parse the current cycle start date
    current_cycle_start = datetime.strptime(current_cycle_start, "%Y-%m-%d")
    
    # Next expected period
    next_cycle_start = current_cycle_start + timedelta(days=cycle_length)

    LUTEAL_LENGTH=14
    # Ovulation day is 14 days before next period
    ovulation_day = next_cycle_start - timedelta(days=LUTEAL_LENGTH)
    
    # Follicular phase: from current cycle start to day before ovulation
    follicular_end = ovulation_day - timedelta(days=1)
    
    # Luteal phase: from ovulation to day before next cycle
    luteal_start = ovulation_day
    luteal_end = next_cycle_start - timedelta(days=1)
    
    # Print results
    print("Upcoming Menstrual Cycle Phases:")
    print(f"Follicular Phase: {current_cycle_start.date()} to {follicular_end.date()}")
    print(f"Ovulation Day: {ovulation_day.date()}")
    print(f"Luteal Phase: {luteal_start.date()} to {luteal_end.date()}")

# Example usage
calculate_future_cycle_phases(current_cycle_start="2025-05-01", cycle_length=35)
