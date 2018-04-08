import xml.etree.ElementTree as ET

#source XML
xml_tree = ET.parse('xml_model.xml')
xml_root = xml_tree.getroot()

inserts = []

for setlist in xml_root:
    insert = {}
    insert['showDate'] = setlist.get('eventDate')

    for venue in setlist.findall('venue'):
        insert['venue'] = venue.get('name')
    inserts.append(insert)



for show in inserts:
    print(show)


