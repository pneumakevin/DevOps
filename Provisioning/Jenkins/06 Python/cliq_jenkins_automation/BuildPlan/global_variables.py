import time
'''==================================
Build Plan Variables
   ==================================
'''


'''====================================
Configuration
-Folder Vairables : 
 Manualy configure it in accordance with actual folders or files you want to include or exclude. 
 it will not be updated at run-time.
   ====================================
'''
global _BUILD_SRC_REPOSITORY 
#_BUILD_SRC_REPOSITORY = 'C:\Jenkins_Git_Repositiry\SequoiaWebSite'
_BUILD_SRC_REPOSITORY = 'D:\Projects\Sandbox\SequoiaWebSite'
global _BUILD_FOLDERS_EXCLUDED 
_BUILD_FOLDERS_EXCLUDED = ('.', '.git', '.vs', '.svn', 'obj', 'bin', 'font', 'images', 'temp', 'download', 'media', 'Properties')
#folders_included = ('')
global _BUILD_FILE_EXT_INCLUDED 
_BUILD_FILE_EXT_INCLUDED =  ('.sln', '.cs', '.csproj', '.xml', '.snk', '.dll', '.user', '.ashx', '.aspx', '.html', '.htm', '.css', '.config', '.zip')
#build_file_ext_includes = ['*.sln', '*.cs', '*.csproj', '*.xml', '*.snk', '*.dll', '*.user', '*.ashx', '*.aspx', '*.html', '*.htm', '*.css', '*.config', '*.zip','*.doc', '*.odt'] # for files only
#excludes = ['/home/paulo-freitas/Documents'] # for dirs and files

global _PRIMARY_PRJ
_PRIMARY_PRJ = ['Sequoia.CliqStudios', 'Sequoia.SixSquare', 'Sequoia.Admin']
shared_prj = ['Sequoia.Shared']
sql_folder_prefix = 'Sequoia.6square.Database.'

'''==================================
Configuration
-Dynamic Variables
 Manualy configure it in accordance with actual folders or files you want to include or exclude. 
 it WILL BE UPDATED at run-time.
   ==================================
'''
# Will be updated after build job successful at runtime.
_BUILD_SRC_LAST_UPDATE_DATE = time.strptime( '2017-10-10 00:00:00', "%Y-%m-%d %H:%M:%S")
# Value will be added from .csprojc at runtime.
primary_references = {'Sequoia.CliqStudios':'', 'Sequoia.SixSquare':'', 'Sequoia.Admin': ''}

