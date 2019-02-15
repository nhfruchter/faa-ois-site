from faadata import *

def mock(empty=False):
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
  
	sampleZero = {'status': {'code': 200, 'info': 'OK', 'count': 0},
	 				'GroundDelays': {'groundDelay': [], 'count': 0},
					'GroundStops': {'groundStop': [], 'count': 0},
					'ArriveDepartDelays': {'arriveDepart': [], 'count': 0},
					'Closures': {'closure': [], 'count': 0}}
	if empty:
		return parseFAA(sampleZero)
	else:	
		return parseFAA(sample)