import pytz
import pandas as pd
from datetime import datetime, timezone

def get_timenow_awere():
	time_zone = pytz.timezone('Europe/Paris')
	# Get the current UTC time
	now = pd.to_datetime(datetime.now(tz=timezone.utc))

	# Make it timezone aware
	now = now.replace(tzinfo=pytz.utc).astimezone(time_zone)

	return now