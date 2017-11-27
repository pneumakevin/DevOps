'''
Created on Nov 2, 2017

@author: kevinchen
'''
from stat import S_ISREG, ST_CTIME, ST_MODE
import sys,time, datetime
import os, os.path
import re, stat
import BuildPlan.global_variables  as gvars
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree.ElementTree as ET
from operator import itemgetter
from BuildPlan.BuildTask import BuildTask
from BuildPlan.SourceTask import SourceTask
from BuildPlan.Modules.Common import prettify
from subprocess import check_output
import subprocess


# if __name__ == '__main__':
#     #check_output("dir C:", shell=False).decode()
#     #proc = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
#     #stdout, stderr = proc.communicate('dir c:\\')
#     proc = subprocess.call("cmd.exe /c msbuild.exe C:\\Jenkins_Git_Repositiry\\SequoiaWebSite\\Sequoia.Utility\\Sequoia.Utility.csproj  /p:Configuration=Release")
#     print ("return code: {}".format(proc))
    
if __name__ == '__main__':
    '''
    Experiment SourceTask
    Purpose: Find modification files which has the date greater than last updates.
    '''
    print("'''\n=============================================\n{}\n=============================================\n'''".format("Experiment SourceTask\n Purpose: Find modification files which has the date greater than last updates."))
    srcTask = SourceTask()
    srcTask.analyze()
    '''
    Return modification files of each projects
    '''
    print("Modification files list group by projects ==>")
    for cdate, file in srcTask.ModifiedFiles:
        print("    {}".format(file) )
    ''' Extract filepath from returned list '''
    modified_projects =  [ os.path.dirname(file) for cdate, file in srcTask.ModifiedFiles]
    ''' Remove duplicated project '''
    modified_projects = list(set(modified_projects))
    print("===============")
      
    ''' 
    Trim base directory from each project path, 
    remove '\' symbol from at first character of path and
    ignore path with 0 length of element in list
    '''
    modified_projects = [ (item[1:] ) for item in  
                            [(item.replace( gvars._BUILD_SRC_REPOSITORY, '') )  for item in modified_projects] 
                            if (item.find('\\',1) and len(item)>0) ]                             
    '''Trim '\\' at the first of string '''
    #modified_projects = [  (item[1:] )  for item in modified_projects if (item.find('\\',1) or item !=[]) ] 
    print ("Projects which has file modified ==>")
    print ("    {}".format(modified_projects))
    print("===============")
       
    '''
    Experiment BuildTask
    Purpose: Build a tree of project dependency in xml format
    '''
    print("'''\n=============================================\n{}\n=============================================\n'''".format("Experiment BuildTask\n Purpose: Build a tree of project dependency in xmal format."))
    buildtask = BuildTask(modified_projects)
    '''
    TODO:
    1. Write modified flag for each projects according to file modification sate at runtime
    2. Once build plan has generated, plug build plan in Jenkins job
      
    '''
    proj_dependencies_tree = buildtask.build_proj_tree()
    print('{}'.format('The project dependency tree ==>'))
    #xmldata = prettify(proj_dependencies_tree) 
    print( prettify(proj_dependencies_tree)  )
    print("===============")  
      
      
    '''
    Experiment build orders of BuildTask
    Purpose: Generate build plan
    '''
    print("'''\n=============================================\n{}\n=============================================\n'''".format("Experiment build orders of BuildTask\n Purpose: Generate build plan."))
    #proj_dependency_tree = ET.fromstring(xmldata)
    deploylist=[]
    primary_ref_list = []
    primary_list = [item.attrib for item in proj_dependencies_tree.findall('./primary')]
    print("Primary project list:{}".format(primary_list))
    print("===============")
         
    '''
    1. if any level of parent project has modifications, build parent will also build all childs which have modifications.
    1.1 else build each individual projct of childs seperately
    2. deploy all updated dll to each target websites.
    '''
    #proj_has_modifications= ['Sequoia.DataCommand', 'Sequoia.Utility']
    #proj_has_modifications= ['Sequoia.DataCommand', 'Sequoia.Utility', 'Sequoia.Payment']
  
    #proj_has_modifications = ['Sequoia.CliqStudios', 'Sequoia.Admin','Sequoia.Utility']
    #proj_has_modifications = ['Sequoia.CliqStudios']
    proj_has_modifications = modified_projects
      
    buildplan = []
    buildtask = BuildTask()
    for modi_proj in proj_has_modifications:
        parent_list = buildtask.find_proj_parent(proj_dependencies_tree, modi_proj, deploylist)  
        deploylist = [dict(y) for y in set(tuple(x.items()) for x in deploylist)]
        deploylist = list({ v['name']:v for v in deploylist}.values())
        for item in sorted(deploylist,key=itemgetter('level'), reverse=False):
            print ( item )
            buildplan.append(item)
        print("+++++++++++++")
        #primary_ref_list.append( sorted(deploylist,key=itemgetter('level'), reverse=False) )
        #deploylist.clear()
  
    buildplan = [dict(y) for y in set(tuple(x.items()) for x in buildplan)]
    buildplan = list({ v['name']:v for v in buildplan}.values())
    print("The build plan ==>\n")
    for proj in buildplan:
        print("    {}".format(proj['name']))
    for proj in buildplan:   
        print("Building projct: {}".format(proj['name'])) 
        proc = subprocess.call("cmd.exe /c msbuild.exe {0}\\{1}\\{1}.csproj  /p:Configuration=Release".format(gvars._BUILD_SRC_REPOSITORY, proj['name'] ))
        print ("return code: {}".format(proc))
     
#     deploymentplan = []
#     for key in buildplan:    
#         for primary in gvars._PRIMARY_PRJ:
#             buildit = False
#             buildtask.find_proj_child(primary, proj_dependencies_tree, buildit)
#             if buildit == True:
#                 deploymentplan.append(primary) 
        
    
# if __name__ == '__main__':
#     '''
#     Experiment parsing project reference in .csproj file
#     Purpose: Parse project dependencies according to .csproj
#     '''
#     buildtask = BuildTask()
#     buildtask.parse_proj_dependency(gvars._PRIMARY_PRJ)


#      
# if __name__ == '__main__':
#  
#     buildtask = BuildTask()
#     proj_dependencies_tree = buildtask.build_proj_tree()
#     print( prettify(proj_dependencies_tree)  )  
    
#     for nodes in buildtask.build_proj_tree() :
#         for atag in nodes:
#             print ("==> " + str(atag.attrib))


# if __name__ == '__main__':
#     '''
#     Experiment build orders of BuildTask
#     Purpose: Generate build plan
#     '''
#     xmldata = """
#         <projroot>
#             <primary name="Sequoia.CliqStudios" level="1" modified="True">
#                 <sub name="Sequoia.DataCommand" level="2" modified="True"></sub>
#                 <sub name="Sequoia.Site" level="2" modified="True">
#                     <sub name="Sequoia.DataCommand" level="3" modified="True"></sub>
#                     <sub name="Sequoia.Payment" level="3" modified="True">
#                         <sub name="Sequoia.DataCommand" level="4" modified="True"></sub>
#                         <sub name="Sequoia.Utility" level="4" modified="True"></sub>
#                     </sub>
#                     <sub name="Sequoia.Utility" level="3" modified="True">
#                         <sub name="Sequoia.DataCommand" level="4" modified="True"></sub>
#                     </sub>
#                 </sub>
#                 <sub name="Sequoia.Utility" level="2" modified="True">
#                     <sub name="Sequoia.DataCommand" level="3" modified="True"></sub>
#                 </sub>
#             </primary>
#             <primary name="Sequoia.Admin" level="1" modified="True">
#                 <sub name="Sequoia.DataCommand" level="2" modified="True"></sub>
#                 <sub name="Sequoia.Logistic" level="2" modified="True"></sub>
#                 <sub name="Sequoia.Site" level="2" modified="True"></sub>
#                 <sub name="Sequoia.Utility" level="2" modified="True"></sub>
#             </primary>
#             <primary name="Sequoia.AsyncWS" level="1" modified="True">
#             </primary>
#         </projroot>
#         """
#     tree = ET.fromstring(xmldata)
#     deploylist=[]
#     primary_ref_list = []
#     primary_list = [item.attrib for item in tree.findall('./primary')]
#     print("Primary project list:{}".format(primary_list))
#     print("===============")
#         
#     '''
#     1. if any level of parent project has modifications, build parent will also build all childs which have modifications.
#     1.1 else build each individual projct of childs seperately
#     2. deploy all updated dll to each target websites.
#     '''
# #     proj_has_modifications= ['Sequoia.DataCommand', 'Sequoia.Utility']
# #     #proj_has_modifications = ['Sequoia.CliqStudios', 'Sequoia.Admin','Sequoia.Utility']
# #     #proj_has_modifications = ['Sequoia.CliqStudios']
# #     buildtask = BuildTask()
# #     for modi_proj in proj_has_modifications:
# #         parent_list = buildtask.find_proj_parent(tree, modi_proj, deploylist)
# #         for item in sorted(deploylist,key=itemgetter('level'), reverse=False):
# #             print ( item )
# #         print("+++++++++++++")
# #         primary_ref_list.append( sorted(deploylist,key=itemgetter('level'), reverse=False) )
# #         deploylist.clear()
#         
#     #print (set(primary_ref_list))