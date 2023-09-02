import json
from datetime import datetime
import time
import requests

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

def is_on_time(stop_number, hour, minute):
    result = False
    
    response = requests.get("https://api.at.govt.nz/serviceinfo/v1/departures/" + stop_number + "?scope=tripsData&subscription-key=****")
    # print (response.text)
    data = json.loads(response.text)

    movements = data['response']['movements']
    time.sleep(5)

    #print(data['response']['movements'])
    for movement in movements:
        
        date_object = datetime.strptime(movement['scheduledArrivalTime'], "%Y-%m-%dT%H:%M:%S.000Z")
        #print(str(datetime_from_utc_to_local(date_object).minute) + " " + str(datetime_from_utc_to_local(date_object).hour) + " " + movement['stop_code'])
        if str(datetime_from_utc_to_local(date_object).hour) == hour and str(datetime_from_utc_to_local(date_object).minute) == minute:
            if movement['arrivalStatus'] == "cancelled":
                result = False
            else:
                result = True
            
    return result

out_text = ""

both_on_time = (is_on_time("1234", "8", "00") and is_on_time("4321", "19", "00"))
if both_on_time:
    out_text = "The bus and train are OK :)"
else:
    out_text = "Bus or train are late or cancelled :("

requests.post("https://ntfy.sh/****",
  data=out_text.encode(encoding='utf-8'))
