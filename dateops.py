#!/usr/bin/env python
"""
dateStamp() return current date in YYYY-MM format
e.g.    2018-09-29

dateTimeStamp() return the current date and time in YYYY-MM-DD_HH-MM format
e.g.  2018-09-29_18-55
"""
from datetime import datetime


def dateStamp():
    start_time = datetime.now()
    start_string = start_time.strftime("%Y-%m-%d")
    return start_string


def dateTimeStamp():
    start_time = datetime.now()
    start_string = start_time.strftime("%Y-%m-%d_%H-%M")
    return start_string


def main():
    print(dateStamp())
    print(dateTimeStamp())


if __name__ == "__main__":
    main()
