#!/usr/bin/python3
import requests
import xml.etree.ElementTree as ET

tree = ET.parse('sample.xml')
root = tree.getroot()

for item in root.findall("./"):
	print(item.attrib)
	for x in item:
		print(x.attrib)

