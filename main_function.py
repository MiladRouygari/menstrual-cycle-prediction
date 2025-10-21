from phase_prediction import classify_phase
import learning_content_suggestion
from phase_utils import consistent_phase


def predict_phase_day_and_content(
    mucus_today: str,
    cycle_day: int, # Today_cycle_day --- this number is from 1 to cycle_length (for irregular cycle, it might exceed cycle_length)
    prev_day_in_phase: int, # This number is from 1 to length of the current phase # check PHASE_CYCLE_LENGTHS from learning_content_suggestion.py
    cycle_length: int = 28,
    prev_phase: str | None = None, # This is given from running the function yesterday
    mucus_today_weight: float = 1.0,
    mucus_vs_day_weight: float = 0.6,
):
    
    # 1) Predict today's phase from inputs
    raw_phase = classify_phase(
        mucus_today=mucus_today,
        cycle_day=cycle_day, 
        cycle_length=cycle_length,
        mucus_today_weight=mucus_today_weight,
        mucus_vs_day_weight=mucus_vs_day_weight,
    )
    #print("Raw predicted phase:", raw_phase)

    # 2) Make it consistent with yesterday phase
    final_phase = consistent_phase(prev_phase, raw_phase) if prev_phase else raw_phase
    #print("Final predicted phase:", final_phase)
    
    # reset the day_in_phase counter if phase changed
    if final_phase == prev_phase:
        day_in_phase = prev_day_in_phase + 1
    else:
        day_in_phase = 1

    # The learning content suggestion
    content_id = learning_content_suggestion.learning_content(final_phase, day_in_phase)
    return final_phase, day_in_phase, content_id


# example usage:
phase, day_in_phase, content_id = predict_phase_day_and_content(
    mucus_today='sticky',
    cycle_day=8,
    prev_day_in_phase=7,
    cycle_length=28,
    prev_phase="EF",
)
print(phase, day_in_phase, content_id)
