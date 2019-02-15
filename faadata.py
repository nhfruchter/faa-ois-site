import requests
from datetime import datetime

ENDPOINT = "https://soa.smext.faa.gov/asws/api/airport/delays"

def fetch():
	"""Fetch data from FAA airport status web service and package for site."""
	
	data = getData()
	if 'error' in data:
		return data
	else:
		return parseFAA(data)

def getData():
	"""Grab data from FAA endpoint in JSON."""
	
	data = requests.get(ENDPOINT, json=True)
	
	if data.status_code == 200:
		return data.json()
	else:
		return {
			'error': 'Data is currently unavailable from the FAA.', 
			'code': data.status_code, 
			'ts': datetime.now().isoformat() 
		}	

def parseFAA(data):
	"""Extract useful data from API response and add translations."""
	
	output = {}
	output['total'] = data['status'].get('count') or 0
	output['ts'] = datetime.now().isoformat()
	
	# Ground delays
	nGroundDelays = data['GroundDelays']['count']
	output['groundDelays'] = {'n': nGroundDelays, 'items': [] }
	if nGroundDelays: 
		for gd in data['GroundDelays']['groundDelay']:
			gd['parsedReason'], gd['parsedExplanation'] = parseReason(gd['reason'])
			output['groundDelays']['items'].append(gd)

	# Ground stops
	nGroundStops = data['GroundStops']['count']
	output['groundStops'] = {'n': nGroundStops, 'items': [] }
	if nGroundDelays: 
		for gs in data['GroundStops']['groundStop']:
			gs['parsedReason'], gs['parsedExplanation'] = parseReason(gs['reason'])
			output['groundStops']['items'].append(gs)
		
	# Arr/dep delays		
	nADDelays = data['ArriveDepartDelays']['count']
	output['arriveDepart'] = {'n': nADDelays, 'items': [] }
	if nADDelays: 
		for ad in data['ArriveDepartDelays']['arriveDepart']:
			ad['parsedReason'], ad['parsedExplanation'] = parseReason(ad['reason'])
			output['arriveDepart']['items'].append(ad)
			
	# Closures
	nClosures = data['Closures']['count']
	output['closures'] = {'n': nClosures, 'items': [] }
	if nClosures: 
		for cl in data['Closures']['closure']:
			cl['parsedReason'], cl['parsedExplanation'] = parseReason(cl['reason'])
			output['closures']['items'].append(cl)
	
	return output
			
def parseReason(reason):
	"""
	Transform a `reason` string from the API to remove FAA formatting 
	and abbreviations, plus add explanations for certain terms.
	"""
	
	exps = {
		'wx': "Inclement weather can affect visibility, safety, and many other factors.",
		'ceil': "A low 'ceiling' of clouds affects visibility, so airports may slow or stop aircraft movements.",
		'rwy': "There is an advisory related to one or more of the runways.",
		'vol': "The volume of traffic is too high for the airport to handle given the current conditions, so movements may be delayed.",
		'thunder': "Aircraft cannot arrive or depart through certain types of thunderstorms, so they will often cause delays.",
		'swap': "There's severe weather in the area that can't be flown through, so this may cause delays in the airspace nearby.",
		'tm': "Air traffic control has changed normal traffic patterns to manage changes in the airspace.",
		'construction': "Air traffic control is working around construction at the airport."
	}
	
	reason = reason.upper()
	explanations = []
	
	# Standardize separator
	reason = reason.replace(" / ", "/")
	reason = reason.replace(":", "/")
	reason = reason.replace("/", " / ")
	
	# Abbreviations
	reason = reason.replace("WEATHER", "Weather")
	reason = reason.replace("WX", "Weather")	
	reason = reason.replace("RWY", "Runway" )
	reason = reason.replace("RY ", "Runway ")
	reason = reason.replace("TM ", "Traffic management ")
	reason = reason.replace("INITIATIVES", "")
	reason = reason.replace("SWAP", "Severe weather avoidance")
	reason = reason.replace("CONSTRUCTION", "Construction")
	if "VOL" in reason: explanations.append(exps['vol'])
	reason = reason.replace("VOL", "Aircraft volume")
	reason = reason.replace("VOLUME", "Aircraft volume")
	reason = reason.replace("MULTITAXI", "High volume of taxiing aircraft")
	
	# Weather explanations
	reason = reason.replace("LOW CEILINGS", "Low Ceilings")
	reason = reason.replace("WIND", "Wind")
	reason = reason.replace("TSTMS", "Thunderstorms")
	reason = reason.replace("THUNDERSTORMS", "Thunderstorms")
	
	
	if "management" in reason: explanations.append(exps['tm'])
	if "Weather" in reason: explanations.append(exps['wx'])
	if "Ceiling" in reason: explanations.append(exps['ceil'])
	if "Runway" in reason: explanations.append(exps['rwy'])
	if "Thunder" in reason: explanations.append(exps['thunder'])
	if "Severe" in reason: explanations.append(exps['swap'])
	if "Construction" in reason: explanations.append(exps['construction'])
	
	return reason,explanations

def mock():
	sample = {'status': {'code': 200, 'info': 'OK', 'count': 9},
 'GroundDelays': {'groundDelay': [{'airport': 'LAS',
    'avgTime': '1 hour and 41 minutes',
    'reason': 'WEATHER / LOW CEILINGS'},
   {'airport': 'PHX',
    'avgTime': '44 minutes',
    'reason': 'WEATHER / LOW CEILINGS'},
   {'airport': 'SFO',
    'avgTime': '1 hour and 32 minutes',
    'reason': 'Weather / WIND'},
   {'airport': 'LAX', 'avgTime': '45 minutes', 'reason': 'RWY / CONSTRUCTION'},
   {'airport': 'JFK',
    'avgTime': '2 hours and 30 minutes',
    'reason': 'WX / THUNDERSTORMS'}],
  'count': 5},
 'GroundStops': {'groundStop': [{'airport': 'DFW',
    'endTime': '1830',
    'reason': 'AAL ONLY / SOFTWARE OUTAGE'}],
  'count': 1},
 'ArriveDepartDelays': {'arriveDepart': [{'airport': 'LAS',
    'maxTime': '30 minutes',
    'reason': 'WX:Wind',
    'minTime': '16 minutes'},
   {'airport': 'PIT',
    'maxTime': '45 minutes',
    'reason': 'WX:TM Initiatives:SWAP',
    'minTime': '2 hours 30 minutes'}],
  'count': 2},
 'Closures': {'closure': [{'airport': 'HNL',
    'reason': 'WX:Hurricane',
    'reopen': '09/25/2018'}],
  'count': 1}}

	return parseFAA(sample)

