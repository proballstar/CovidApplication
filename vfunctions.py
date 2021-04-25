import requests

def get_req(url):
  r = requests.get(url)
  if r.status_code == 200:
    return r.json()
  else:
    raise Exception('the request did not get through')

def binary_search(city, data):  
  low = 0
  high = len(data) 
  while (low <= high):
    mid = (low+high) // 2
    if (data[mid]['city'].upper() == city.upper()):
      return data[mid]
    if (data[mid]['city'].upper() < city.upper()):
      low = mid + 1
    else:
      high = mid - 1
  
  return -1

def parse_vaccines(data: dict, state: str, city: str):
  global state_dict
  state_dict = data['responsePayloadData']['data'][state]
  return binary_search(city, state_dict)