THRESHOLD = 100.0


def detect_anomaly(units, prev_units):
    """Simple anomaly detection for energy usage.

    Args:
        units (float): Current usage.
        prev_units (float|None): Previous usage for same device.

    Returns:
        str: One of "cyber_threat", "fault", or "normal".
    """

    if prev_units is not None and units > prev_units * 2:
        return "cyber_threat"

    if units > THRESHOLD:
        return "fault"

    return "normal"
