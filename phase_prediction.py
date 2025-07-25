from phase_utils import *


def classify_phase(
    mucus_today,
    mucus_yesterday,
    cycle_day,
    cycle_length=28,
    mucus_today_weight=0.7,
    mucus_yesterday_weight=0.5,
    mucus_vs_day_weight=0.5  
):
    mucus_phase_scores = {
        'none':     {'EF': 1.0, 'OV': 0.2, 'EL': 0.7, 'LL': 0.7},
        'sticky':   {'EF': 1.0, 'LF': 1.0, 'OV': 0.2, 'EL': 0.7, 'LL': 0.7},
        'creamy':   {'LF': 1.0, 'LF': 0.5},
        'egg white':{'OV': 1.0, 'LF': 0.3},
        'watery':   {'OV': 1.0},
    }

    phase_day_ranges = get_phase_day_ranges(cycle_length)
    print(phase_day_ranges)
    

    phase_scores = {}
    score_breakdown = {}  # <-- dictionary to store mt, my, d scores

    for phase in phase_day_ranges:
        mt_score = mucus_phase_scores.get(mucus_today, {}).get(phase, 0.0)
        my_score = mucus_phase_scores.get(mucus_yesterday, {}).get(phase, 0.0)

        mucus_score = (
            mucus_today_weight * mt_score +
            mucus_yesterday_weight * my_score
        )

        d_score = day_match_score(cycle_day, phase, phase_day_ranges)

        total_score = (
            mucus_vs_day_weight * mucus_score +
            (1 - mucus_vs_day_weight) * d_score
        )

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
