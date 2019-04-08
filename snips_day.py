import datetime
from dateutil import tz
from pprint import pprint

def get_local_time(utc_time):
  from_zone = tz.tzutc()
  to_zone = tz.tzlocal()
  utc = datetime.datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S+00:00")
  utc = utc.replace(tzinfo=from_zone)
  local = utc.astimezone(to_zone)
  time = local.strftime("%H:%M")
  #print(time)
  return time
