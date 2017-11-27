@ECHO OFF
ECHO Preparing to deploy Sequoia.AsyncWS
SET SiteName=cliqtest
SET Websvc=cliqws
SET SiteAdmin=admin
SET SEQUOIA_ASYNCWS_PROJ=Sequoia.AsyncWS
SET SEQUOIA_ADMIN_PROJ=Sequoia.Admin
SET WebsvcPackageFolderPath=C:\Jenkins_Git_Repositiry\SequoiaWebSite\%SEQUOIA_ASYNCWS_PROJ%
SET TargetFolderPath=C:\Sequoia\%SEQUOIA_ASYNCWS_PROJ%
SET AdminPackageFolderPath=C:\Jenkins_Git_Repositiry\SequoiaWebSite\%SEQUOIA_ADMIN_PROJ%
SET AdminTargetFolderPath=C:\Sequoia\%SEQUOIA_ADMIN_PROJ%
SET appcmd=CALL %WINDIR%\system32\inetsrv\appcmd
SET ipaddr=172.30.9.19
SET username=jenkins
SET password=P@ssw0rd123
ECHO Building %WebsvcPackageFolderPath% as local files
cd %WebsvcPackageFolderPath%
msbuild %SEQUOIA_ASYNCWS_PROJ%.csproj /p:DeployOnBuild=true /p:Configuration=Release;PackageLocation=%SEQUOIA_ASYNCWS_PROJ%Pacakge-Release.zip /P:DeployIISAppPath=%Websvc% /p:AuthType=NTLM
REM /p:PublishProfile=FolderPublish 

REM msbuild %SEQUOIA_ASYNCWS_PROJ%.csproj /t:package /p:Configuration=Release;PackageLocation=%SEQUOIA_ASYNCWS_PROJ%Pacakge-Release.zip 

ECHO Local deploying %SEQUOIA_ASYNCWS_PROJ% to %Websvc%
cd %WebsvcPackageFolderPath%
REM "C:\Program Files (x86)\IIS\Microsoft Web Deploy V3\msdeploy.exe" -verb:sync -source:contentPath=%WebsvcPackageFolderPath% -dest:contentPath=%TargetFolderPath%
REM "C:\Program Files (x86)\IIS\Microsoft Web Deploy V3\msdeploy.exe" -verb:sync -source:package=%SEQUOIA_ASYNCWS_PROJ%Pacakge-Release.zip -dest:apphostconfig=%Websvc%

%SEQUOIA_ASYNCWS_PROJ%Pacakge-Release.deploy.cmd /Y /M:http://%ipaddr%/MsDeployAgentService /U:%username% /P:%password%

ECHO Exiting from preparing deploy Sequoia.AsyncWS



