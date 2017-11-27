'''
Created on Nov 2, 2017

@author: kevinchen
'''
import sys,time, datetime
import os, os.path
import re
from stat import *
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree.ElementTree as ET
from operator import itemgetter
import BuildPlan.global_variables as gvars

class SourceTask(object):
    '''
    classdocs
    '''
    _modified_files = []


    def __init__(self, modified_files = []):
        '''
        Constructor
        '''
        self._modified_files = modified_files
        
    @property
    def ModifiedFiles(self):
        return self._modified_files

    @ModifiedFiles.setter
    def ModifiedFiles(self, value):
        self._modified_files = value
        
#    @staticmethod
#     def analyze():
#         #f = open("C:\\Users\\kevinchen\\Desktop\\Current Works\\Python\\filelist.txt", "w") 
#         f = open("D:\\_Current Works\\Python\\cliq_jenkins_automation\\BuildPlan\\modified_file_list.txt", "w+")
#         #with open("C:\\Users\\kevinchen\\Desktop\\Current Works\\Python\\filelist.txt", "w+") as f:    
#         for path, subdirs, files  in os.walk(gvars._BUILD_SRC_REPOSITORY, topdown=True):
#             # exclude dirs
#             #subdirs[:] = [os.path.join(path, d) for d in subdirs]
#             #subdirs[:] = [d for d in subdirs if not re.match(gvars._BUILD_FOLDERS_EXCLUDED, d)]
#             subdirs[:] = [d for d in subdirs if not d.startswith(gvars._BUILD_FOLDERS_EXCLUDED)]
#             #print( subdirs)
#             # exclude/include files
#             files = [os.path.join(path, f) for f in files if f.endswith( gvars._BUILD_FILE_EXT_INCLUDED) ]
#             #files = [f for f in files if not re.match(excludes, f)]
#             #files = [f for f in files if re.match(includes, f)]
#             # get all files in the directory w/ stats
#             #print (files)
#             files = [ (os.stat(path),path) for path in files ]
#             #print (files)
#             # leave only regular files, insert creation date
#             #files = [( time.localtime(ST_CTIME), path) for stat, path in sorted(files,reverse=True) if S_ISREG(ST_MODE )]
#             #files = [( time.ctime(ST_CTIME), path) for stat, path in sorted(files,reverse=True) if S_ISREG(ST_MODE )]
#             files = [( time.localtime(stat[ST_CTIME]), path) for stat, path in sorted(files,reverse=True) ]
#             #print (files)
#             #NOTE: on Windows `ST_CTIME` is a creation date 
#             #  but on Unix it could be something else
#             #NOTE: use `ST_MTIME` to sort by a modification date    
#             files = [ (cdate, path )for (cdate, path) in files if cdate > gvars._BUILD_SRC_LAST_UPDATE_DATE ]
#             #print (files)
#             for cdate, path in files:
#                 f_state_path = time.strftime( "%Y-%m-%d %H:%M:%S", cdate  ), path
#                 print (f_state_path)
#                 f.write(str(f_state_path) +"\n")
#                 #print ("path=>" + path)
#                 #input()
#     
#         f.close()

    #@staticmethod
    def analyze(self):
        #f = open("C:\\Users\\kevinchen\\Desktop\\Current Works\\Python\\filelist.txt", "w") 
        fhandler = open("D:\\_Current Works\\Python\\cliq_jenkins_automation\\BuildPlan\\modified_file_list.txt", "w+")
        #fhandler = open("C:\\Jenkins_node\\Provisioning\\Python\\cliq_jenkins_automation\\BuildPlan\\modified_file_list.txt", "w+")
        #with open("C:\\Users\\kevinchen\\Desktop\\Current Works\\Python\\filelist.txt", "w+") as f:    
#         for path, subdirs, files  in os.walk(gvars._BUILD_SRC_REPOSITORY, topdown=True):
#             # exclude dirs
#             subdirs[:] = [d for d in subdirs if not d.startswith(gvars._BUILD_FOLDERS_EXCLUDED)]
#             for d in subdirs :
#                 pathname = os.path.join(path, d)
#                 SourceTask.__walktree(pathname, fhandler)
        #SourceTask.__walktree(gvars._BUILD_SRC_REPOSITORY, fhandler)
        self.__walktree(gvars._BUILD_SRC_REPOSITORY, fhandler)
        fhandler.close()   
    
    #@staticmethod    
    def __walktree(self, topdir, fhandler):
        '''recursively descend the directory tree rooted at top,
           calling the callback function for each regular file'''
        for path, subdirs, files  in os.walk(topdir, topdown=True):
            # exclude dirs
            #subdirs[:] = [os.path.join(path, d) for d in subdirs]
            #subdirs[:] = [d for d in subdirs if not re.match(gvars._BUILD_FOLDERS_EXCLUDED, d)]
            subdirs[:] = [d for d in subdirs if not d.startswith(gvars._BUILD_FOLDERS_EXCLUDED)]
            for adir in subdirs:
                #SourceTask.__walktree(adir, fhandler )
                self.__walktree(adir, fhandler )
            #print( subdirs)
            # exclude/include files
            files = [os.path.join(path, f) for f in files if f.endswith( gvars._BUILD_FILE_EXT_INCLUDED) ]
            #files = [f for f in files if not re.match(excludes, f)]
            #files = [f for f in files if re.match(includes, f)]
            # get all files in the directory w/ stats
            #print (files)
            files = [ (os.stat(path),path) for path in files ]
            #print (files)
            # leave only regular files, insert creation date
            #files = [( time.localtime(ST_CTIME), path) for stat, path in sorted(files,reverse=True) if S_ISREG(ST_MODE )]
            #files = [( time.ctime(ST_CTIME), path) for stat, path in sorted(files,reverse=True) if S_ISREG(ST_MODE )]
            files = [( time.localtime(stat[ST_CTIME]), path) for stat, path in sorted(files,reverse=True) ]
            #print (files)
            #NOTE: on Windows `ST_CTIME` is a creation date 
            #  but on Unix it could be something else
            #NOTE: use `ST_MTIME` to sort by a modification date    
            files = [ (cdate, path )for (cdate, path) in files if cdate > gvars._BUILD_SRC_LAST_UPDATE_DATE ]
            #print (files)
            for cdate, path in files:
                f_state_path = time.strftime( "%Y-%m-%d %H:%M:%S", cdate  ), path
                #print (f_state_path)
#                 SourceTask._modified_files.append(f_state_path)
#                 print( SourceTask._modified_files)
                self.ModifiedFiles.append(f_state_path)
                #print( self.ModifiedFiles)
                fhandler.write(str(f_state_path) +"\n")
                


                
    def visitfile(self, file):
        print ('visiting', file)
    
    @staticmethod    
    def setfilesinfo(self, files):   
        files = [os.path.join(path, f) for (path,f) in files if f.endswith( gvars._BUILD_FILE_EXT_INCLUDED) ]
        files = [ (os.stat(path),path) for path in files ]
        #print (files
        files = [(time.localtime(stat[ST_CTIME]), path) for stat, path in sorted(files,reverse=True) ]
        #print (files)
        #NOTE: on Windows `ST_CTIME` is a creation date 
        #  but on Unix it could be something else
        #NOTE: use `ST_MTIME` to sort by a modification date    
        files = [(cdate, path ) for (cdate, path) in files if cdate > gvars._BUILD_SRC_LAST_UPDATE_DATE ]
        #print (files
            
        