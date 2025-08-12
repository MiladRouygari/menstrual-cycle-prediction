def get_phase_day_ranges(cycle_length):

    """
    Divides a menstrual cycle into phase-specific day ranges based on the total cycle length.

    The function splits the cycle into the following phases:
        - EF (Early Follicular)
        - LF (Late Follicular)
        - OV (Ovulation)
        - EL (Early Luteal)
        - LL (Late Luteal)

    Fixed durations:
        - OV (Ovulation): 5 days
        - EL (Early Luteal): 5 days
        - LL (Late Luteal): 7 days

    The remaining days (after allocating OV, EL, and LL) are flexibly distributed between EF and LF 
    in a 7:4 ratio.

    Parameters:
        cycle_length (int): Total number of days in the cycle.

    Returns:
        dict: A dictionary mapping each phase name ('EF', 'LF', 'OV', 'EL', 'LL') 
              to a corresponding range of days (1-indexed).

    Example:
        >>> get_phase_day_ranges(28)
        {
        'EF': range(1, 8),
        'LF': range(8, 12),
        'OV': range(12, 17),
        'EL': range(17, 22),
        'LL': range(22, 29),
    }
    """
    # Fixed phase durations
    ov_len = 5
    el_len = 6 
    ll_len = 6 
    fixed_len = ov_len + el_len + ll_len

    
    # Flexible days go to EF and LF
    flexible_len = cycle_length - fixed_len

    # Split EF and LF in 7:4 ratio
    ef_len = round(flexible_len * 7 / 11)
    lf_len = flexible_len - ef_len

    # Build the ranges step by step
    ef_start = 1
    ef_end = ef_start + ef_len - 1

    lf_start = ef_end + 1
    lf_end = lf_start + lf_len - 1

    ov_start = lf_end + 1
    ov_end = ov_start + ov_len - 1

    el_start = ov_end + 1
    el_end = el_start + el_len - 1

    ll_start = el_end + 1
    ll_end = cycle_length

    return {
        'EF': range(ef_start, ef_end + 1),
        'LF': range(lf_start, lf_end + 1),
        'OV': range(ov_start, ov_end + 1),
        'EL': range(el_start, el_end + 1),
        'LL': range(ll_start, ll_end + 1),
    }


def get_phase_lengths(cycle_length):
    """
    Returns the length (number of days) of each menstrual cycle phase 
    based on the provided cycle length.

    Parameters:
        cycle_length (int): Total number of days in the cycle.

    Returns:
        dict: A dictionary mapping each phase name ('EF', 'LF', 'OV', 'EL', 'LL') 
              to the number of days in that phase.
    """
    day_ranges = get_phase_day_ranges(cycle_length)
    return {phase: len(days) for phase, days in day_ranges.items()}


def day_match_score(day, phase, phase_day_ranges):
    """
    Calculates a score indicating how well a given day aligns with the expected day range for a specific phase.

    If the day falls within the day range associated with the given phase, the score is 1.0.
    Otherwise, the score decreases linearly by 0.2 for each day of distance from the closest day in the range,
    with a minimum score of 0.0.

    Parameters:
        day (int): The day to evaluate.
        phase (str): The name of the phase whose day range should be used for comparison.
        phase_day_ranges (dict): Dictionary mapping phase names to ranges of days.

    Returns:
        float: A score between 0.0 and 1.0 indicating how closely the day matches the expected phase day range.
    """
    if day in phase_day_ranges[phase]:
        return 1.0
    else:
        min_dist = min(abs(day - d) for d in phase_day_ranges[phase])
        return max(0.0, 1 - 0.2 * min_dist)
    

def get_stage(cycle_day: int, cycle_length: int) -> str:
    
    """
    Determine the menstrual cycle stage based on the given cycle day and cycle length.

    This function categorizes the current stage of a menstrual cycle into one of three phases:
    'pre-ovulation', 'ovulation', or 'post-ovulation', based on mappings between the cycle length
    and estimated ovulation window.

    Parameters:
        cycle_day (int): The current day in the menstrual cycle
        cycle_length (int): The total length of the menstrual cycle (must be between 23 and 35 inclusive).

    Returns:
        str: The stage of the menstrual cycle, one of 'pre-ovulation', 'ovulation', or 'post-ovulation'.
    """

    # Ovulation stage mapping
    # Mapping of cycle length to corresponding ovulation window (start day, end day)
    ovulation_stage_days = {
        23: (7, 13), # the first interation was (7,17)
        24: (8, 14), 
        25: (9, 15), 
        26: (10, 16), 
        27: (11, 17), 
        28: (12, 18), 
        29: (13, 19), 
        30: (14, 20), 
        31: (15, 21), 
        32: (16, 22), 
        33: (17, 23), 
        34: (18, 24),
        35: (18, 25), 
    }

    # Retrieve the ovulation window based on the given cycle length
    start_ov, end_ov = ovulation_stage_days[cycle_length]

    # Determine the stage based on the current cycle day
    if cycle_day < start_ov:
        return 'pre-ovulation'
    elif start_ov <= cycle_day <= end_ov:
        return 'ovulation'
    else:
        return 'post-ovulation'


def get_weights(cycle_day: int, cycle_length: int) -> dict:
    
    """
    Return the cervical mucus scoring weights based on the appropriate stage (pre-, ovulation, post-ovulation) 
    of the menstrual cycle.
    
    This function determines the current stage of the cycle using the given cycle day and cycle length,
    and returns a dictionary of mucus types mapped to their corresponding weights during that stage.

    The weights are organized as follows:
        - For 'pre-ovulation': Emphasizes early Follicular (EF) and Late Follicular (LF).
        - For 'ovulation': Emphasizes ovulation (OV) and transition phases (EL, LL).
        - For 'post-ovulation': Primarily maps to Luteal (EL, LL).

    Parameters:
        cycle_day (int): The current day in the menstrual cycle.
        cycle_length (int): The total length of the menstrual cycle.

    Returns:
        dict: A dictionary mapping mucus types (e.g., 'creamy', 'egg white') to fertility score weights 
              (e.g., {'EF': 1.0, 'LF': 0.8}), based on the determined stage.

    """
    # Define weights for each mucus type based on the current stage of the cycle
    stage_mucus_scores = {
    'pre-ovulation': {
        'none': {'EF': 1.0, 'LF': 0.8},
        'sticky': {'EF': 1.0, 'LF': 0.8},
        'creamy': {'LF': 0.5},
        'egg white': {'LF': 0.3},
        'watery': {'EF': 0.4, 'LF': 0.7}, 
    },
    'ovulation': { # if by "mistake" they put "None" or "Sticky" they will get EL
        'none': {'LF': 0.4,'EL': 0.5},
        'sticky': {'LF': 0.4, 'EL': 0.5},
        'creamy': {'LF': 0.4},
        'egg white': {'OV': 0.7},
        'watery': {'OV': 1.0},
    },
    'post-ovulation': { 
        'none': {'EL': 0.7, 'LL': 0.7},
        'sticky': {'EL': 0.7, 'LL': 0.7},
        'creamy': {},
        'egg white': {'OV': 1.0,'EL': 0.5, 'LL': 0.5}, # OV have some weights so the first days of post-ovulation stage could potentially be OV
        'watery': {'OV': 1.0, 'EL': 0.5, 'LL': 0.5},    
    },
}

    # Determine the current stage of the cycle
    stage = get_stage(cycle_day, cycle_length)

    # Return the corresponding mucus weight dictionary for that stage
    return stage_mucus_scores.get(stage, {}) 


def consistent_phase(prev_phase, today_phase):
    """
    Returns the more consistent phase between a previous day's phase and today's predicted phase,
    based on a predefined sequential order of phases.

    Phases must either stay the same or progress forward. Any backward steps are 
    considered inconsistent, and the previous phase is returned.

    IMPORTANT: Jumps are possible!! (e.g, two or more step forward, 'EF' to 'OV')

    Parameters:
        prev_phase (str): The predicted phase from the previous day.
        today_phase (str): The predicted phase for today.

    Returns:
        str: The consistent phase, either the same as or one step after the previous phase.
    """
    phase_order = ['EF', 'LF', 'OV', 'EL', 'LL']
    prev_index = phase_order.index(prev_phase)
    today_index = phase_order.index(today_phase)

    if today_index >= prev_index:
        return today_phase
    else:
        return prev_phase



