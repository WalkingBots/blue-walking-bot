import config
import json
import time
from datetime import datetime
import os
import csv

datadir = os.path.join(os.path.expanduser('~'), 'data', config.name.lower().replace(' ', '_'))
if not os.path.exists(datadir): os.makedirs(datadir)

with open(os.path.join(datadir,'dump.csv'), mode='w') as csv_file:
    logf = csv.writer(csv_file)
    logf.writerow(["id","longitude","latitude","timestamp","filetype","username"])
	
def fnpath(username, ts, ft, fmt):
	return os.path.join(datadir, '{0}_{1}_{2}.{3}'.format(username, ts, ft, fmt))
	
#locf = open(fnpath(username, ts, filetype, 'csv'), 'w')
def data_with_location(filetype, data, username, location):
#	 logf = open(os.path.join(datadir,'dump.csv'), 'a')
	with open(os.path.join(datadir,'dump.csv'), mode='a') as csv_file:
		logf = csv.writer(csv_file)
   
		print('going to save data', filetype, data, username, location)
		ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
		if filetype == 'photo':
			f = fnpath(username, ts, filetype, 'jpg')
			data.download(f)
		elif filetype == 'voice':
			f = fnpath(username, ts, filetype, 'ogg')	
			data.download(f)
		elif filetype == 'text':
			f = fnpath(username, ts, filetype, 'txt')
			with open(f) as textf:
				textf.write(data)
		else:
			f = ''
			raise TypeError('wrong filetype')
	#		 locf.write(json.dumps({'filename': f,
	#								'longitude': location.longitude,
	#								'latitude': location.latitude,
	#								'timestamp': ts,
	#								'filetype': filetype,
	#								'username': username}, indent=2))
		logf.writerow([str(f), str(location.longitude), str(location.latitude), str(ts), str(filetype), str(username)])
		csv_file.flush()
	
def voice_source_peaks_location(voice, peaks, source, location, username):
    with open(os.path.join(datadir,'dump.csv'), mode='a') as csv_file:
        logf = csv.writer(csv_file)
        print('going to save data', peaks, source, username, location)
        ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
        f = fnpath(username, ts, 'voice', 'ogg')
        voice.download(f)
	#		 locf.write(json.dumps({'filename': f,s
	#								'longitude': location.longitude,
	#								'latitude': location.latitude,
	#								'timestamp': ts,
	#								'filetype': filetype,
	#								'username': username}, indent=2))
        logf.writerow([str(f), str(location.longitude), str(location.latitude), str(ts), 'voice', source, peaks, str(username)])
        csv_file.flush()