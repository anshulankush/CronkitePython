from urllib2 import Request, urlopen
import xml.etree.ElementTree as ET
import json


url_request = Request('http://inciweb.nwcg.gov/feeds/rss/incidents/state/3')
try:
    url_response = urlopen(url_request)
    rss_content = url_response.read()
except Exception as e:
    print(str(e))

xml_root = ET.fromstring(rss_content)
incidents_dict = {}
incidents = []

for xml_child in xml_root:
    for item_child in xml_child.findall("item"):
        incidents_dict['title'] = item_child.find('title').text
        incidents_dict['link'] = item_child.find('link').text
        incidents_dict['description'] = item_child.find('description').text
        incidents_dict['pubDate'] = item_child.find('pubDate').text
        geo_namespaces = {'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#'}
        incidents_dict['lat'] = item_child.find('geo:lat', namespaces=geo_namespaces).text
        incidents_dict['long'] = item_child.find('geo:long', namespaces=geo_namespaces).text
        incidents.append(incidents_dict)

json_formatted_string = "callback({\"incidents\": " + str(json.dumps
             (incidents, indent=4, skipkeys=True, sort_keys=True) + "});")
try:
    filename = "./wildfire01.json"
    fob = open(filename, 'rU')
    old_json_string = fob.read()
    fob.close()
    if old_json_string != json_formatted_string:
        fd = open(filename, 'w')
        print(json_formatted_string)
        fd.write(json_formatted_string)
        fd.close()
except Exception as e:
    print ('ERROR writing: {}'.format(e))
