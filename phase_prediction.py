from phase_utils import *


def classify_phase(
    mucus_today,
    mucus_yesterday,
    cycle_day,
    cycle_length,
    mucus_today_weight=0.7,
    mucus_yesterday_weight=0.5,
    mucus_vs_day_weight=0.5  
):
    """
    Estimates the most likely menstrual cycle phase based on cervical mucus observations and cycle day.

    This function combines two scoring methods:
    1. Mucus-based scoring: Evaluates how typical the current and previous day's cervical mucus 
       types are for each phase.
    2. Day-based scoring: Assesses how well the current cycle day aligns with typical timing of each phase.

    These scores are weighted and combined to determine the most probable phase.

    Parameters:
        mucus_today (str): Type of cervical mucus observed today (e.g., 'none', 'sticky', 'creamy', 'egg white', 'watery').
        mucus_yesterday (str): Type of cervical mucus observed yesterday.
        cycle_day (int): Current day in the menstrual cycle.
        cycle_length (int): Total length of the cycle.
        mucus_today_weight (float, optional): Weight of today's mucus in the mucus score. Defaults to 0.7.
        mucus_yesterday_weight (float, optional): Weight of yesterday's mucus in the mucus score. Defaults to 0.5.
        mucus_vs_day_weight (float, optional): Relative weight of mucus vs. day score in total score. Defaults to 0.5.

    Returns:
        str: The name of the most likely phase, one of: 
             'EF' (Early Follicular), 'LF' (Late Follicular), 'OV' (Ovulation), 
             'EL' (Early Luteal), or 'LL' (Late Luteal).

    Notes:
        - The function currently returns only the top-scoring phase. To enable debug information,
          uncomment the detailed return dictionary at the bottom of the function.

    Example:
        >>> classify_phase('creamy', 'sticky', cycle_day=12, ,cycle_length=30)
        'LF'
    """
    # Define how different types of cervical mucus are associated with each phase
    # Scores indicate how typical each mucus type is for each phase
    mucus_phase_scores = {
        'none':     {'EF': 1.0, 'OV': 0.2, 'EL': 0.7, 'LL': 0.7},
        'sticky':   {'EF': 1.0, 'LF': 1.0, 'OV': 0.2, 'EL': 0.7, 'LL': 0.7},
        'creamy':   {'LF': 1.0, 'LF': 0.5},
        'egg white':{'OV': 1.0, 'LF': 0.3},
        'watery':   {'OV': 1.0},
    }

    # Get day ranges for each phase based on the cycle length
    phase_day_ranges = get_phase_day_ranges(cycle_length)
    # print(phase_day_ranges) # Debug print
    
    # # Dictionaries to store final scores and intermediate breakdowns
    phase_scores = {}
    score_breakdown = {}  # dictionary to store mt, my, d scores / For diagnostics and debugging

    # Compute a score for each phase based on mucus and day matching
    for phase in phase_day_ranges:
        mt_score = mucus_phase_scores.get(mucus_today, {}).get(phase, 0.0)
        my_score = mucus_phase_scores.get(mucus_yesterday, {}).get(phase, 0.0)

        # Weighted mucus score using today's and yesterday's mucus
        mucus_score = (
            mucus_today_weight * mt_score +
            mucus_yesterday_weight * my_score
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
            "my_score": my_score,
            "d_score": round(d_score, 2),
            "mucus_score": round(mucus_score, 2),
            "total_score": round(total_score, 2)
        }

    # if not phase_scores:
    #     return {"phase": "Unknown", "confidence": 0.0, "scores": {}}

    best_phase = max(phase_scores, key=phase_scores.get)


    return best_phase
    
    # debugging purpose 
    # Optional: return more detailed information for debugging
    # return {
    #     "phase": best_phase,
    #     "confidence": round(phase_scores[best_phase], 2),
    #     "scores": score_breakdown
    # }

# Example usage
print(classify_phase(
    mucus_today='None',
    mucus_yesterday='None',
    cycle_day=1,
    cycle_length=35)
    )
