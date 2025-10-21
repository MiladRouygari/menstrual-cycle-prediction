from phase_prediction import classify_phase
import learning_content_suggestion
from phase_utils import consistent_phase


def predict_phase_day_and_content(
    mucus_today: str,
    cycle_day: int, # Today’s cycle day (1..cycle_length; may exceed for irregular cycles)
    prev_day_in_phase: int, # Days spent in the *previous* phase up to yesterday
    cycle_length: int = 28,
    prev_phase: str | None = None, # Phase predicted yesterday (None if unknown)
    mucus_today_weight: float = 1.0,
    mucus_vs_day_weight: float = 0.6,
):
    """
    Predict today's cycle phase, update the day-in-phase counter, and return a learning
    content suggestion that matches the phase/day.

    This function:
      1) Predicts today's raw phase using `classify_phase` based on today's mucus,
        day within the cycle, and model weights.
      2) Makes the raw prediction consistent with yesterday's phase using
         `consistent_phase` (prevents unrealistic jumps between phases).
      3) Resets or increments the `day_in_phase` counter depending on whether the
         phase changed.
      4) Retrieves a content ID tailored to the resulting phase/day via
         `learning_content_suggestion.learning_content`.

    Parameters
    ----------
    mucus_today : str
        Qualitative mucus observation for today (e.g., "none", "sticky", "creamy", ...).
        Valid values must match what `classify_phase` expects.
    cycle_day : int
        Today's cycle day. May exceed `cycle_length` for irregular cycles.
    prev_day_in_phase : int
        The number of days spent in the *previous* phase as of yesterday (>= 1).
        This is used to increment the counter if the phase remains the same today.
        See `PHASE_CYCLE_LENGTHS` in `learning_content_suggestion.py` for context.
    cycle_length : int, optional
        Nominal cycle length (default 28). Passed through to `classify_phase`.
    prev_phase : str | None, optional
        Yesterday's phase label. If provided, we will enforce consistency relative
        to this phase. If `None`, the raw prediction is used as-is ('None' for the 1st day of the month).
    mucus_today_weight : float, optional
        Weight for today's mucus observation in `classify_phase` (default 1.0).
    mucus_vs_day_weight : float, optional
        Weight for cycle-day-based likelihood in `classify_phase` (default 0.6).

    Returns
    -------
    tuple[str, int, str]
        A 3-tuple of:
          - final_phase : str
                The phase predicted for today after consistency adjustment.
          - day_in_phase : int
                The day index within the current phase. Resets to 1 when
                the phase changes; otherwise increments from `prev_day_in_phase`.
          - content_id : str
                An identifier of learning content suggested for `(final_phase, day_in_phase)`.

    Notes
    -----
    - `consistent_phase(prev_phase, raw_phase)` is only applied when `prev_phase` is not None.
    - This function does not validate value ranges; any validation should be handled
      by callers.    
    """
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
    
    # 3) Update the day-in-phase counter:
    # reset the day_in_phase counter if phase changed
    if final_phase == prev_phase:
        day_in_phase = prev_day_in_phase + 1
    else:
        day_in_phase = 1

    # 4) Select learning content tailored to today's phase/day
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
