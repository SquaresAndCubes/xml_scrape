from lxml import objectify

root = objectify.XML('xml_model.xml')

print(root["setlist"])


