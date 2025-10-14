from phase_utils import *


def classify_phase(
    mucus_today,
    cycle_day,
    cycle_length=28,
    mucus_today_weight=1,
    mucus_vs_day_weight=0.6  
):
    """
    Estimates the most likely menstrual cycle phase based on cervical mucus observations and cycle day.

    This function combines two scoring methods:
    1. Mucus-based scoring: Evaluates how typical the current day's cervical mucus 
       types are for each phase.
    2. Day-based scoring: Assesses how well the current cycle day aligns with typical timing of each phase.

    These scores are weighted and combined to determine the most probable phase.

    Parameters:
        mucus_today (str): Type of cervical mucus observed today (e.g., 'none', 'sticky', 'creamy', 'egg white', 'watery').
        cycle_day (int): Current day in the menstrual cycle.
        cycle_length (int): Total length of the cycle.
        mucus_today_weight (float, optional): Weight of today's mucus in the mucus score. Defaults to 1.
        mucus_vs_day_weight (float, optional): Relative weight of mucus vs. day score in total score. Defaults to 0.5.

    Returns:
        str: The name of the most likely phase, one of: 
             'EF' (Early Follicular), 'LF' (Late Follicular), 'OV' (Ovulation), 
             'EL' (Early Luteal), or 'LL' (Late Luteal).

    Notes:
        - The function currently returns only the top-scoring phase. To enable debug information,
          uncomment the detailed return dictionary at the bottom of the function.
    """

    # Scores how different types of cervical mucus are associated with each stage
    mucus_phase_scores = get_weights(cycle_day, cycle_length)
    #print(mucus_phase_scores) # Debug print

    # Get day ranges for each phase based on the cycle length
    phase_day_ranges = get_phase_day_ranges(cycle_length)
    # print(phase_day_ranges) # Debug print
    
    # # Dictionaries to store final scores and intermediate breakdowns
    phase_scores = {}
    score_breakdown = {}  # dictionary to store mt, my, d scores / For diagnostics and debugging

    # Compute a score for each phase based on mucus and day matching
    for phase in phase_day_ranges:
        mt_score = mucus_phase_scores.get(mucus_today, {}).get(phase, 0.0)

        # Weighted mucus score using today's mucus
        mucus_score = (
            mucus_today_weight * mt_score
        )
        # How well the current day aligns with the given phase
        d_score = day_match_score(cycle_day, phase, phase_day_ranges)

        # Combine mucus and day-based scores
        total_score = (
            mucus_vs_day_weight * mucus_score +
            (1 - mucus_vs_day_weight) * d_score
        )

        # Store final score for the phase
        phase_scores[phase] = total_score

        # Save individual scores for analysis
        score_breakdown[phase] = {
            "mt_score": mt_score,
            "d_score": round(d_score, 2),
            "mucus_score": round(mucus_score, 2),
            "total_score": round(total_score, 2)
        }


    best_phase = max(phase_scores, key=phase_scores.get)


    return best_phase
    
    # debugging purpose 
    # Optional: return more detailed information for debugging
    return {
        "phase": best_phase,
        "confidence": round(phase_scores[best_phase], 2),
        "scores": score_breakdown
    }

# Example usage
print(classify_phase(
    mucus_today=' ',
    cycle_day=8,
    cycle_length=28
))

###### Testing all the possible combinatinons of day and mucuses (5 per day) ######
import pandas as pd

# Load the CSV file
cycle_length=35
mucus_vs_day_weight=0.5
df = pd.read_csv(f'csv_files/day_mucus_combinations_cycle_length_{cycle_length}.csv')  # Adjust path if needed
# Apply the function to each row
df['predicted_phase'] = df.apply(
    lambda row: classify_phase(
        mucus_today=row['today_mucus'],
        cycle_day=row['day'],
        cycle_length=cycle_length,
        mucus_vs_day_weight=mucus_vs_day_weight
    ),
    axis=1
)

# Save the result to a new CSV
df.to_csv(f'csv_files/day_mucus_combinations_with_predicted_phase_cycle_length_{cycle_length}_mucus_vs_day_weight_{mucus_vs_day_weight}.csv', index=False)
