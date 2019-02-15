import requests
from datetime import datetime

ENDPOINT = "https://soa.smext.faa.gov/asws/api/airport/delays"

def hasMosaicATM(iata):
	SUPPORTED = ['ATL', 'BWI', 'DCA', 'DTW', 'HNL', 'IAH', 'LAX', 'MDW', 'MKE', 'PHL', 'SAN', 'SFO',
	 			 'STL', 'BDL', 'CLE', 'DEN', 'EWR', 'HOU', 'JFK', 'LGA', 'MEM', 'MSP', 'PHX', 'SDF',
				 'SLC', 'BOS', 'CLT', 'DFW', 'FLL', 'IAD', 'LAS', 'MCO', 'MIA', 'ORD', 'PVD', 'SEA',
				 'SNA']
	
	
	iata = iata.upper()
	if iata == "HNL":
		return "PHNL"
	else:
		if iata in SUPPORTED:
			return "K{0}".format(iata)
		else:
			return False				

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
			gd['mosaic'] = hasMosaicATM(gd['airport'])
			output['groundDelays']['items'].append(gd)
			
	# Ground stops
	nGroundStops = data['GroundStops']['count']
	output['groundStops'] = {'n': nGroundStops, 'items': [] }
	if nGroundStops: 
		for gs in data['GroundStops']['groundStop']:
			gs['parsedReason'], gs['parsedExplanation'] = parseReason(gs['reason'])
			gs['mosaic'] = hasMosaicATM(gs['airport'])
			output['groundStops']['items'].append(gs)
		
	# Arr/dep delays		
	nADDelays = data['ArriveDepartDelays']['count']
	output['arriveDepart'] = {'n': nADDelays, 'items': [] }
	if nADDelays: 
		for ad in data['ArriveDepartDelays']['arriveDepart']:
			ad['parsedReason'], ad['parsedExplanation'] = parseReason(ad['reason'])
			ad['mosaic'] = hasMosaicATM(ad['airport'])			
			output['arriveDepart']['items'].append(ad)
			
	# Closures
	nClosures = data['Closures']['count']
	output['closures'] = {'n': nClosures, 'items': [] }
	if nClosures: 
		for cl in data['Closures']['closure']:
			cl['parsedReason'], cl['parsedExplanation'] = parseReason(cl['reason'])
			cl['mosaic'] = hasMosaicATM(cl['airport'])
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
		'construction': "Air traffic control is working around construction at the airport.",
		'mt': "Airport runways and taxiways can get congested just like busy roads at rush hour."
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
	if "VOL" in reason: 
		explanations.append(exps['vol'])
		reason = reason.replace("UME", "")
	reason = reason.replace("VOL ", "Aircraft volume ")
	reason = reason.replace("VOLUME", "Aircraft volume")
	reason = reason.replace("MULTITAXI", "High volume of taxiing aircraft")
	reason = reason.replace("MULTI TAXI", "High volume of taxiing aircraft")
	reason = reason.replace("MULTI-TAXI", "High volume of taxiing aircraft")
	
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
	if "taxiing" in reason: explanations.append(exps['mt'])
	return reason,explanations


