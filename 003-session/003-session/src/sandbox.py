from pprint import pprint as pp
import googlemaps

# gmaps = googlemaps.Client(key=open('.api_key').read())
#
# route = gmaps.distance_matrix(origins=['University of Tehran, Tehran, Tehran Province'],
#                               destinations=['Sharif University of Technology, Tehran'],
#                               mode='driving', language='English', units='metric')
# pp(route)
# {'destination_addresses' : ['Tehran, Azadi Avenue، Iran'],
#  'origin_addresses'    : ['Tehran, Tehran Province, Iran'],
#  'rows'                : [{'elements': [{'distance': {'text': '7.8 km', 'value': 7755},
#                          'duration': {'text': '14 mins', 'value': 868},
#                          'status': 'OK'}]}],
#  'status': 'OK'}

# from dis import dis, show_code
# def harchi(x):
#     return [str(i ** 2) for i in range(x) if i != 3] + range(100)
#
#
# dis(harchi)
# show_code(harchi)