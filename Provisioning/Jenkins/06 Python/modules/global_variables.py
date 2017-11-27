import time
'''==================================
Build Plan Variables
   ==================================
'''


'''====================================
Folder Vairables
   ====================================
'''
build_src_repository = 'D:\Projects\Sandbox\SequoiaWebSite'
build_folders_excluded = ('.', '.git', '.vs', '.svn','obj','bin','font', 'images', 'temp')
#folders_included = ('')
build_file_ext_included =  ('.sln', '.cs', '.csproj', '.xml', '.snk', '.dll', '.user', '.ashx', '.aspx', '.html', '.htm', '.css', '.config', '.zip')
#build_file_ext_includes = ['*.sln', '*.cs', '*.csproj', '*.xml', '*.snk', '*.dll', '*.user', '*.ashx', '*.aspx', '*.html', '*.htm', '*.css', '*.config', '*.zip','*.doc', '*.odt'] # for files only
#excludes = ['/home/paulo-freitas/Documents'] # for dirs and files

primary_prj = ['Sequoia.CliqStudios', 'Sequoia.SixSquare', 'Sequoia.Admin']
shared_prj = ['Sequoia.Shared']
sql_folder_prefix = 'Sequoia.6square.Database.'

'''==================================
Dynamic Variables
   ==================================
'''
# Will be updated after build job successful at runtime.
build_src_last_update_date = time.strptime( '2017-10-10 00:00:00', "%Y-%m-%d %H:%M:%S")
# Value will be added from .csprojc at runtime.
primary_references = {'Sequoia.CliqStudios':'', 'Sequoia.SixSquare':'', 'Sequoia.Admin': ''}

