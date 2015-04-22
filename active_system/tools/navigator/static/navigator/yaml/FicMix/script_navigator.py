
from os import listdir
from os.path import isfile, join
import requests
import json

import yaml
	

duration = None
start = None
firstName = None
lastName = None

path = "/home/sviluppo/ACTIVE_workspace/web_tools/video_viewer/yaml/FicMix/"


files = [ f for f in listdir(path) if isfile(join(path,f)) ]
end_point = "http://156.148.132.79:8000/api/people/"
tag_end_point = "http://156.148.132.79:8000/api/tags/"

print files

for f in files:
	in_file = open(join(path,f),"r")
	text = in_file.read()
	dict = yaml.load(text)
	last_name = dict["ann_tag"].split("_")[0]
	first_name = dict["ann_tag"].split("_")[1]
	#print last_name, first_name
	r = requests.post(end_point, data = {"first_name":first_name, "last_name":last_name, "category": "person"} )
	item_id = 1146
	person = json.loads(r.text)
	print person
	for s in dict["segments"]:
		start = int(s["segment_start"])
		duration = int(s["segment_duration"])
		res = requests.post(tag_end_point, data = {"entity_id": person["id"], "item_id":item_id, "start":start, "duration":duration})
		print res.text
		
	
			
	

   
    

