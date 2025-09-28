from datetime import datetime, date as date_type, timedelta
from fastapi import HTTPException

def validate_date(date_str: str) -> date_type:
    """
    Validate and parse a date string in YYYY-MM-DD format.

    Args:
        date_str: Date string to validate.

    Returns:
        date: Parsed date object.

    Raises:
        HTTPException: If the date string is not in the correct format.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid date format",
                "reason": "Use YYYY-MM-DD format"
            }
        )


def validate_date_range(date_str: str, earliest_date: str, days: int = 2) -> date_type:
    """
    Validate date and check if it's within acceptable range.
    Range: from earliest_date up to 2 days before today

    Args:
        date_str: Date to validate in YYYY-MM-DD format
        earliest_date: Earliest allowed date in YYYY-MM-DD format
        days: Number of days before today that is the latest allowed date (default is 3, meaning up to 2 days before today)

    Returns:
        Validated date object

    Raises:
        HTTPException: If date is invalid or out of range
    """
    # Validate input date
    validated_date = validate_date(date_str)

    # Validate and parse earliest date
    try:
        earliest = datetime.strptime(earliest_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Invalid earliest_date parameter",
                "reason": "earliest_date must be in YYYY-MM-DD format"
            }
        )

    # Calculate latest allowed date (2 days before today)
    today = datetime.now().date()
    latest_allowed = today - timedelta(days=days)

    # Check if date is too early
    if validated_date < earliest:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Date too early",
                "reason": f"Date must be on or after {earliest_date}"
            }
        )

    # Check if date is too recent (less than 2 days ago)
    if validated_date > latest_allowed:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Date too recent",
                "reason": f"Date must be at least 2 days before today (on or before {latest_allowed.strftime('%Y-%m-%d')})"
            }
        )

    return validated_date