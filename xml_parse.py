import xml.etree.ElementTree as ET
from lxml import objectify

#source XML
xml_tree = ET.parse('xml_model.xml')
xml_root = xml_tree.getroot()

inserts = []

