from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

top = Element('top')

#comment = Comment('Generated for PyMOTW')
#top.append(comment)

child = SubElement(top, 'child')
#child.text = 'This child contains text.'

child = SubElement(top, 'child')
child.set('name' , "proj1" )
child.set('level', "1")
child = SubElement(child, 'child')
child.set('name' , "proj2" )
child.set('level', "2")


print (prettify(top))