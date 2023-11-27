from datetime import datetime, timedelta
import pytz

def convert_utc_to_manila(utc_str):
    """Convert UTC to Manila Time; Display in 12H format"""
    # Adjust for excessive fractional second digits
    if '.' in utc_str:
        parts = utc_str.split('.')
        fractional_seconds = parts[1][:6]  # Keep up to 6 digits for microseconds
        utc_str = parts[0] + '.' + fractional_seconds

    # Parse the UTC datetime string
    if utc_str.endswith('Z'):
        utc_str = utc_str[:-1] + '+00:00'
    utc_dt = datetime.fromisoformat(utc_str)

    # Set the timezone to UTC if not already set
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=pytz.UTC)

    # Convert to Manila timezone
    manila_tz = pytz.timezone('Asia/Manila')
    manila_dt = utc_dt.astimezone(manila_tz)

    # Format the datetime to a more readable format
    readable_string = manila_dt.strftime('%Y-%m-%d %I:%M:%S %p')

    return readable_string