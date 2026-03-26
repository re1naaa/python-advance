import datetime

current_datetime = datetime.datetime.now()

print("Year:", current_datetime.year)
print("Month:", current_datetime.month)
print("Day:", current_datetime.day)
print("Hour:", current_datetime.hour)
print("Minute:", current_datetime.minute)
print("Second:", current_datetime.second)
print("Microsecond:", current_datetime.microsecond)

current_date = datetime.datetime.now().date()

print("Year:", current_date.year)
print("Month:", current_date.month)
print("Day:", current_date.day)

current_time = datetime.datetime.now().time()

# Define a specific time
time_object = datetime.time(12, 30, 45, 123456)

print("Hour:", time_object.hour)
print("Minute:", time_object.minute)
print("Second:", time_object.second)
print("Microsecond:", time_object.microsecond)

specific_date = datetime.date(2024, 4, 5)
print(specific_date)

specific_time = datetime.time(12, 30, 0)

# Create a datetime object
specific_datetime = datetime.datetime(2024, 1, 1, 14, 30, 0)

# Format the datetime object as a string
formatted_date = specific_datetime.strftime('%Y-%m-%d %H:%M:%S')
print(formatted_date)  # Output: 2024-01-01 14:30:00

duration = datetime.timedelta(days=5, hours=3)

# Adding a timedelta to a date
new_date = current_date + duration
print(new_date)

previous_date = current_date - duration
print(previous_date)

utc_time = datetime.datetime.now(datetime.timezone.utc)
print("Current UTC time:", utc_time)

# Define a custom time zone offset of UTC+3 hours
custom_offset = datetime.timedelta(hours=3)

# Get the current time in the custom time zone
custom_time = utc_time.replace(tzinfo=datetime.timezone(custom_offset))
print("Current time in custom time zone (UTC+3):", custom_time)