@ECHO OFF
SETLOCAL
SET WebRoot=Sequoia.CliqStudios
SET DirToBackup=/cygdrive/D/Projects/Sandbox/SequoiaWebSite/%WebRoot%
SET BackupDir=/cygdrive/D/_backup_test/%WebRoot%
REM rsync --rsync-path="mkdir -p %BackupDir%/ && rsync" -av --exclude-from '/cygdrive/D/_Current Works/Python/exclude-list.txt'  %DirToBackup%/ %BackupDir%/

REM rsync --rsync-path="mkdir -p %BackupDir%/ && rsync"  -av --exclude-from '/cygdrive/D/_Current Works/Python/exclude-list.txt' --recursive --update --delete --perms --owner --group --times  %DirToBackup%/ %BackupDir%/
rsync --rsync-path="mkdir -p %BackupDir%/ && rsync" --dry-run  --times  -av --exclude-from '/cygdrive/D/_Current Works/Python/exclude-list.txt' --recursive --update --delete --perms --owner --group --times  --links --safe-links --super --one-file-system --devices %DirToBackup%/ %BackupDir%/ 
