import json
from datetime import datetime, timezone

#open the json file 
with open("sample.json","r") as file:
    #rading JSON from file and parsing it to convert to python object 
    json_file_data = json.load(file)

#type of python object 
print(f"Type of python object: {type(json_file_data)}")
print(f"Printing the object: {json_file_data}")

print(f"\n\nTitle of Photo: {json_file_data["title"]}")
print(f"\nTimestamp of photo: {json_file_data["photoTakenTime"]["timestamp"]}")
print(f"\nFormatted Capture Time: {json_file_data["photoTakenTime"]["formatted"]}")
print(f"\nType of timestamp: {type(json_file_data["photoTakenTime"]["timestamp"])}")

#converting time stamp to int 
timestamp = int(json_file_data["photoTakenTime"]["timestamp"])

#data type after converting 
print(f"New type of timestamp: {type(timestamp)}")

#converting integer timestamp to datetime format
dateobj = datetime.fromtimestamp(timestamp, tz=timezone.utc)

#formate it nicely 
#proper_date = dateobj.strftime('%d-%m-%Y %H:%M:%S')
print(dateobj)
