@ECHO OFF
ECHO Preparing to deploy Sequoia.CliqStudios
SET SiteName=cliqtest
SET Websvc=cliqws
SET SiteAdmin=admin
SET SEQUOIA_CLIQSTUDIOS_PROJ=Sequoia.CliqStudios
SET SEQUOIA_ASYNCWS_PROJ=Sequoia.AsyncWS
SET SEQUOIA_ADMIN_PROJ=Sequoia.Admin
SET PackageFolderPath=C:\Jenkins_Git_Repositiry\SequoiaWebSite\%SEQUOIA_CLIQSTUDIOS_PROJ%
SET WebsvcPackageFolderPath=C:\Jenkins_Git_Repositiry\SequoiaWebSite\%SEQUOIA_ASYNCWS_PROJ%
SET TargetFolderPath=C:\Sequoia\%SEQUOIA_ASYNCWS_PROJ%
SET AdminPackageFolderPath=C:\Jenkins_Git_Repositiry\SequoiaWebSite\%SEQUOIA_ADMIN_PROJ%
SET AdminTargetFolderPath=C:\Sequoia\%SEQUOIA_ADMIN_PROJ%
SET appcmd=CALL %WINDIR%\system32\inetsrv\appcmd
SET ipaddr=172.30.9.19
SET username=jenkins
SET password=P@ssw0rd123


ECHO Building %SiteName% webapp
cd C:\Jenkins_Git_Repositiry\SequoiaWebSite\Sequoia.CliqStudios\
cd %PackageFolderPath%
ECHO Building %SEQUOIA_CLIQSTUDIOS_PROJ% as web-package 
msbuild %SEQUOIA_CLIQSTUDIOS_PROJ%.csproj /t:package /p:Configuration=Release;PackageLocation=%SEQUOIA_CLIQSTUDIOS_PROJ%Pacakge-Release.zip /P:DeployIISAppPath=%SiteName% /p:AuthType=NTLM


ECHO Deploying %SEQUOIA_CLIQSTUDIOS_PROJ% to %SiteName%
cd %PackageFolderPath%
%SEQUOIA_CLIQSTUDIOS_PROJ%Pacakge-Release.deploy.cmd /Y /M:http://%ipaddr%/MsDeployAgentService /U:%username% /P:%password%

ECHO Exiting from preparing to deploy Sequoia.CliqStudios