from datetime import datetime, timedelta
import pytz

def gameTime(time):
   
  time = time.split(' ', 1)[1]

  date_time_string = time

  # replace non-breaking spaces with regular spaces
  date_time_string = date_time_string.replace("\xa0", " ")

  #set date format
  date_format = "%d %b %Y, %H:%M"

  # parse the date string into a datetime object
  eventTime = datetime.strptime(date_time_string, date_format)
  
  now = datetime.now()
  now = now.replace(microsecond=0)

  time_difference = eventTime - now

  # Break down the timedelta into days, hours, minutes, and seconds
  days = time_difference.days
  seconds = time_difference.seconds

  # Use math operations to convert seconds into hours, minutes, and seconds
  minutes, seconds = divmod(seconds, 60)
  hours, minutes = divmod(minutes, 60)

  countdown = ''
  
  if days > 0:
      # code to execute if days are greater than 0
      countdown += str(days) + ' days, '
  if hours > 0:
      # code to execute if hours are greater than 0
      countdown += str(hours) + ' hours, '
  if minutes > 0:
      # code to execute if minutes are greater than 0
      countdown += str(minutes) + ' minutes, '
  if seconds > 0:
      # code to execute if seconds are greater than 0
      countdown += str(seconds) + ' seconds'

  return days, hours, minutes, seconds, countdown