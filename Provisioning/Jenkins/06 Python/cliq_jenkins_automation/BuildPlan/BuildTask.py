'''
Created on Nov 2, 2017

@author: kevinchen
'''
import os.path
import BuildPlan.global_variables  as gvars

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom
from BuildPlan.Modules.Common import prettify

class BuildTask(object):
    '''
    classdocs
    '''

    def __init__(self, modifled_projects = []):
        '''
        Constructor
        '''
        self._modified_projects = modifled_projects
    
#     def __prettify(self, elem):
#         """Return a pretty-printed XML string for the Element.
#         """
#         rough_string = ET.tostring(elem, 'utf-8')
#         reparsed = minidom.parseString(rough_string)
#         return reparsed.toprettyxml(indent="  ")
   
    def __build_proj_tree(self, parent_node, level):
        '''
        private metod
        '''
       
        level += 1
        for refproj in self.__get_proj_dependency( [parent_node.get('name')]):  
            '''
             parent_node.get('projname') returns string type of project name without ".csproj" of extension
            '''
            child_node = SubElement(parent_node, 'sub')
            child_node.set('name', refproj )
            child_node.set('level', str(level))
            modified = refproj in  self._modified_projects # value from file state in local repository of version control  
            child_node.set('modified', str(modified))
            #csprojfile = os.path.join('{}\\{}'.format(gvars._BUILD_SRC_REPOSITORY, refproj)  , '{}.{}'.format(refproj, 'csproj') )
            child_node.set('path', '{}\\{}'.format(gvars._BUILD_SRC_REPOSITORY, refproj) )
            self.__build_proj_tree( child_node, level)
            
            
             
    def build_proj_tree(self):
        '''
        This method generates tree structures like this xml form:
        
        <primary name="Sequoia.CliqStudios" level="1">
            <sub name="Sequoia.DataCommand" level="2"></sub>
            <sub name="Sequoia.Site" level="2">
                <sub name="Sequoia.DataCommand" level="3"></sub>
                <sub name="Sequoia.Payment" level="3">
                    <sub name="Sequoia.DataCommand" level="4"></sub>
                    <sub name="Sequoia.Utility" level="4">
                </sub>
                <sub name="Sequoia.Utility" level="3">
                    <sub name="Sequoia.DataCommand" level="4"></sub>
                </sub>
            </sub>
            <sub name="Sequoia.Utility" level="2">
                <sub name="Sequoia.DataCommand" level="3"></sub>
            </sub>
        </primary>
        <primary name="Sequoia.Admin" level="1">
            <sub name="Sequoia.DataCommand" level="2"></sub>
            <sub name="Sequoia.Logistic" level="2"></sub>
            <sub name="Sequoia.Site" level="2"></sub>
            <sub name="Sequoia.Utility" level="2"></sub>
        </primary>
        .
        .
        .
        
        
        '''
       
        proj_root = Element('projroot') #create root element
        #comment = Comment('Generate a relationship of projects and its referenced projects in tree structures')
        #proj_root.append(comment)
        level = 1
        modified = "False"
        for proj in gvars._PRIMARY_PRJ:         
            primary = SubElement(proj_root, 'primary')
            primary.set('name' , proj )
            primary.set('level', str(level))
            modified = proj in  self._modified_projects # value from file state in local repository of version control  
            primary.set('modified', str(modified))
            #csprojfile = os.path.join('{}\\{}'.format(gvars._BUILD_SRC_REPOSITORY, proj)  , '{}.{}'.format(proj, 'csproj') )
            primary.set('path', ('{}\\{}'.format(gvars._BUILD_SRC_REPOSITORY, proj )))
            self.__build_proj_tree( primary, level)
                

        #print(BuildPlan.Modules.Common.prettify(proj_root))
        return proj_root

    def __get_proj_dependency(self, projname_list = []):
        '''
        Parse ProjectReference elements in .csproj files
        '''
        proj_dependencies = []
        csprojfile = os.path.join('{}\\{}'.format(gvars._BUILD_SRC_REPOSITORY, projname_list[0])  , '{}.{}'.format( projname_list[0], 'csproj') )
        #print('{} depends on:'.format(projname_list[0]))         
        tree = ET.parse(csprojfile)
        root = tree.getroot()
        # Remove the default namespace definition (xmlns="http://some/namespace")
        self.remove_namespace(root, u'http://schemas.microsoft.com/developer/msbuild/2003') 
        
        for nodes in root.findall('.//ProjectReference'):
            for atag in nodes:
                if (atag.tag == "Name"):
                    #print('   {}'.format(atag.text))
                    proj_dependencies.append(atag.text)
        return proj_dependencies
        #self.__get_proj_dependency(proj_dependencies)
            
    def parse_proj_dependency(self, csproject_list):
        '''
        Parse ProjectReference elements in .csproj files
        '''
        for proj in csproject_list :
            filepath = os.path.join('{}\\{}'.format(gvars._BUILD_SRC_REPOSITORY, proj)  , '{}.{}'.format( proj , 'csproj') )
            #print('{} depends on:'.format(proj))
              
            tree = ET.parse(filepath)

            root = tree.getroot()
            # Remove the default namespace definition (xmlns="http://some/namespace")
            self.remove_namespace(root, u'http://schemas.microsoft.com/developer/msbuild/2003') 
            dependencies = []
            for nodes in root.findall('.//ProjectReference'):
                for atag in nodes:
                    if (atag.tag == "Name"):
                        print('   {}'.format(atag.text))
                        filepath = os.path.join('{}\\{}'.format(gvars._BUILD_SRC_REPOSITORY, atag.text)  , atag.text  )
                        dependencies.append(atag.text)
            self.parse_proj_dependency(dependencies)

    def remove_namespace(self, doc, namespace):
        """Remove namespace in the passed document in place."""
        ns = u'{%s}' % namespace
        nsl = len(ns)
        for elem in doc.getiterator():
            if elem.tag.startswith(ns):
                elem.tag = elem.tag[nsl:]
                
                  
    def __parse_proj_dependency(self, proj_name):
        '''
        Parse ProjectReference elements in .csproj files
        '''
        ret_list = []
        for proj in gvars._PRIMARY_PRJ:
            filepath = os.path.join(gvars._BUILD_SRC_REPOSITORY, proj)
            print('{} depends on:'.format(proj))
            tree = ET.parse(filepath)
            doc = tree.getroot()
            proj_ref = doc.find('ProjectReference')
            for ele in proj_ref:
                print (ele.attrib)
        
        
        return ret_list
    
    def find_proj_tree(self, node , attrib , attrib_value):
        root = node.getroot()
        result = root.find(attrib)
        print (result)
        ret_list = []
        return ret_list
    
    def find_proj_parent(self, node, proj_name, the_list):
        #ret_list = []
        #print(pirmary.tag)
        #for sub in node.findall('.//sub[@projname="' + proj_name + '"]'):
        #    print( str(sub.attrib ))
        #    found_list.append(sub.attrib )
        #for item in sorted(found_list, key=itemgetter('level'), reverse=True):
        #    print( "ereh=>" +str(item )+ "\n")
        for child in node.getchildren():
            if not(child.attrib['name'] == proj_name):
                self.find_proj_parent(child, proj_name, the_list)
            elif child.attrib['name'] == proj_name and int(child.attrib['level']) >= 3 :
                the_list.append(node.attrib)
#             else:
#                 #print("parent=> " + str(node.attrib))
#                 the_list.append(node.attrib)
    
        return
    
    def find_proj_child(self, parent, child_name, found=False):

        for child in parent.getchildren():
            if not(child.attrib['name'] == child_name):
                self.find_proj_child(child, child_name, found)
            elif child.attrib['name'] == child_name and int(child.attrib['level']) >= 2 :
                found = True

    
        return