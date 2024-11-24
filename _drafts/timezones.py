from datetime import datetime, timedelta, timezone


def get_current_time_by_utc_offset():
    # Get the current time in UTC as a timezone-aware datetime object
    utc_now = datetime.now(timezone.utc)

    offsets = set()  # To collect unique offsets

    # Calculate current time for each UTC offset
    for i in range(-12, 15):  # From UTC-12 to UTC+14
        offset = timezone(timedelta(hours=i))
        current_time = utc_now.astimezone(offset)  # Convert to the target timezone
        offset_str = (
            f"UTC{'+' if i >= 0 else ''}{i:02d}:00 - {current_time.strftime('%H:%M')}"
        )
        offsets.add(offset_str)  # Add to set for uniqueness

    return sorted(offsets)


# Print the current time for each UTC offset
for offset in get_current_time_by_utc_offset():
    print(offset)
