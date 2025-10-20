# number of learning contents each phase has
PHASE_CYCLE_LENGTHS = {
    "EF": 7,
    "LF": 4,
    "OV": 5,
    "EL": 6,
    "LL": 6,
}

def learning_content(
    phase: str,
    day_in_phase: int,
):
    """
    Return the learning content for a given phase and day.

    Rules:
    - Each phase has a fixed number of content items.
    - If the phase lasts longer than its content length, wrap around to the start.
      e.g. EF day 8 -> same as EF day 1; LF day 5 -> same as LF day 1.
    - Function returns a simple content identifier like "EF_3".
    
    Args:
        phase: One of {"EF","LF","OV","EL","LL"}.
        day_in_phase: 1-based day number within the current phase (must be >= 1).

    Returns:
        a content ID string like "EF_3".

    """

    cycle_len = PHASE_CYCLE_LENGTHS[phase]
    # Wrap day into the cycle length: 
    # Subtracting 1 before the modulo and adding 1 after guarantees the result is always in 1..cycle_len
    content_index = ((day_in_phase - 1) % cycle_len) + 1

    # Return a simple identifier if no concrete content was provided
    return f"{phase}_{content_index}"


# -------------------------
# Examples
# -------------------------

print(learning_content("EF", 1))
print(learning_content("EF", 7))
print(learning_content("EF", 8))
print(learning_content("LF", 8))
