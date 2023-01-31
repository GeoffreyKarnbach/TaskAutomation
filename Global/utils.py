from datetime import datetime

def get_readable_time():
    currentDate = datetime.now()
    date_time = currentDate.strftime("%d/%m/%Y at %H:%M:%S")
    return date_time

def convert_seconds_to_readable_time(seconds):
    # Number of hours
    days = seconds // (24 * 3600)
    hours = (seconds % (24 * 3600)) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return f"{days} days {hours} hours {minutes} minutes and {round(seconds)} seconds"

def is_in_interval(startTime, endTime):
    currentDate = datetime.now()
    date_time = currentDate.strftime("%H:%M")

    start = [int(startTime.split(":")[0]), int(startTime.split(":")[1])]
    end = [int(endTime.split(":")[0]), int(endTime.split(":")[1])]
    current = [int(date_time.split(":")[0]), int(date_time.split(":")[1])]

    if start[0] <= current[0] <= end[0]:
        if start[0] < current[0] < end[0]:
            return True
        elif start[0] == current[0]:
            return start[1] <= current[1]
        elif end[0] == current[0]:
            return end[1] >= current[1]
    
    return False