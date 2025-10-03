"""
Julian Date and Modified Julian Date Converter

This script provides functions to convert a standard Gregorian date and time
into the corresponding Julian Date (JD) and Modified Julian Date (MJD).
These date formats are commonly used in astronomy and scientific applications.

The calculations are based on standard astronomical formulas and rely only on
Python's built-in datetime module.

Usage:
    python julian_date_converter.py
    (Run directly to see the example conversion.)
"""

from datetime import datetime
import sys
from typing import Tuple

# A constant representing the JD of the Unix Epoch (1970-01-01 00:00:00 UTC)
# This is often used as a reference point, but the main calculation uses
# the fixed historical epoch.
JD_OF_UNIX_EPOCH = 2440587.5

def calculate_jd(dt: datetime) -> float:
    """
    Calculates the Julian Date (JD) for a given datetime object.

    The Julian Date is the interval of time in days and fractions of a day since
    January 1, 4713 BC, Greenwich noon (12:00 UT).

    The formula used here is valid for Gregorian dates (after 1582).

    Args:
        dt (datetime): The standard datetime object.

    Returns:
        float: The calculated Julian Date.
    """
    # 1. Separate components
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    microsecond = dt.microsecond

    # 2. Adjust for January (1) and February (2)
    # The calculation assumes March is the first month (M=3), so we adjust
    # M and Y for Jan/Feb.
    if month <= 2:
        year -= 1
        month += 12

    # 3. Calculate A and B (A is the integral part of Y/100, B is the correction)
    # This accounts for the shift from Julian to Gregorian calendar (after 1582)
    A = year // 100
    B = 2 - A + (A // 4)

    # 4. Calculate the Day Fraction (UT day/24 hours)
    day_fraction = (hour + minute / 60 + second / 3600 + microsecond / 3600000000) / 24.0

    # 5. Calculate the Integer Part of the Julian Day Number
    # This part gets the JD at 0h UT (midnight) of the given date.
    jd_integer = (
        (365.25 * (year + 4716)) // 1
        + (30.6001 * (month + 1)) // 1
        + day + B - 1524.5
    )

    # 6. Calculate the Final Julian Date (JD at the exact time)
    # JD is defined as starting at 12:00 UT (noon), hence the 0.5 offset in the integer part.
    # We add the day fraction to the midnight JD number.
    
    # Note: 1524.5 in the formula already accounts for the 0.5 (noon start) relative to midnight calculation.
    jd = jd_integer + day_fraction

    return jd

def calculate_mjd(jd: float) -> float:
    """
    Calculates the Modified Julian Date (MJD) from the Julian Date (JD).

    MJD is simpler, defined as JD - 2400000.5 days. It starts at midnight
    (00:00 UT) rather than noon, which is often more convenient.

    Args:
        jd (float): The Julian Date.

    Returns:
        float: The calculated Modified Julian Date (MJD).
    """
    # MJD epoch is 1858-11-17 00:00:00 UT
    return jd - 2400000.5

def convert_date_to_julian(date_str: str, time_str: str) -> Tuple[float, float]:
    """
    Wrapper function to parse date/time strings and perform both conversions.
    
    Args:
        date_str (str): Date in YYYY-MM-DD format.
        time_str (str): Time in HH:MM:SS format (assuming UTC).

    Returns:
        Tuple[float, float]: (Julian Date, Modified Julian Date)
    """
    try:
        # Create a single datetime object from the parts. Assuming UTC time for standard JD calculation.
        dt_str = f"{date_str} {time_str}"
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        
        jd = calculate_jd(dt)
        mjd = calculate_mjd(jd)
        
        return jd, mjd

    except ValueError:
        print(f"Error: Invalid date or time format. Please use YYYY-MM-DD and HH:MM:SS.")
        sys.exit(1)


def main():
    """Demonstrates the usage of the date conversion functions."""

    print("--- Julian Date Converter Demonstration ---")
    
    # Example 1: Historical Date
    date1 = "2000-01-01"
    time1 = "12:00:00" # Noon UT
    
    jd1, mjd1 = convert_date_to_julian(date1, time1)

    print(f"\nTarget Date (UT): {date1} {time1}")
    print(f"  Julian Date (JD): {jd1:.6f} days") # Expected value: 2451545.0
    print(f"  Modified Julian Date (MJD): {mjd1:.6f} days") # Expected value: 51544.5

    print("-" * 40)
    
    # Example 2: Arbitrary Date and Time (Midnight UT)
    date2 = "2024-10-26"
    time2 = "00:00:00" # Midnight UT
    
    jd2, mjd2 = convert_date_to_julian(date2, time2)
    
    print(f"\nTarget Date (UT): {date2} {time2}")
    print(f"  Julian Date (JD): {jd2:.6f} days") # Expected value: 2460608.5
    print(f"  Modified Julian Date (MJD): {mjd2:.6f} days") # Expected value: 60608.0

    print("-" * 40)
    
    # Example 3: Date with precise time
    date3 = "2024-03-15"
    time3 = "06:30:15" 
    
    jd3, mjd3 = convert_date_to_julian(date3, time3)

    print(f"\nTarget Date (UT): {date3} {time3}")
    print(f"  Julian Date (JD): {jd3:.6f} days")
    print(f"  Modified Julian Date (MJD): {mjd3:.6f} days")

if __name__ == "__main__":
    main()
