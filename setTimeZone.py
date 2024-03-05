from datetime import datetime, timedelta
import pytz

def setTime():
   
  # get current time
  now = datetime.now()

  # set timezone
  timezone = pytz.timezone('Australia/Brisbane')

  # localize the current time
  local_time = timezone.localize(now)

  print(local_time)
   