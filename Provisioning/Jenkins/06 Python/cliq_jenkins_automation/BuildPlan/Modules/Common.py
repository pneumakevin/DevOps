'''
Created on Nov 13, 2017

@author: kevinchen
'''
from xml.etree import ElementTree as ET
from xml.dom import minidom

def prettify( elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="    ")