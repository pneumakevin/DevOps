@ECHO OFF
ECHO Preparing to deploy Sequoia.Admin
SET SiteName=cliqtest
SET SiteAdmin=admin
SET SEQUOIA_ADMIN_PROJ=Sequoia.Admin
SET AdminPackageFolderPath=C:\Jenkins_Git_Repositiry\SequoiaWebSite\%SEQUOIA_ADMIN_PROJ%
SET AdminTargetFolderPath=C:\Sequoia\%SEQUOIA_ADMIN_PROJ%
SET appcmd=CALL %WINDIR%\system32\inetsrv\appcmd
SET ipaddr=172.30.9.19
SET username=jenkins
SET password=P@ssw0rd123

cd %AdminPackageFolderPath%
ECHO Building %SEQUOIA_ADMIN_PROJ% as web-package 
msbuild %SEQUOIA_ADMIN_PROJ%.csproj /p:DeployOnBuild=true /p:Configuration=Release;PackageLocation=%SEQUOIA_ADMIN_PROJ%Pacakge-Release.zip /P:DeployIISAppPath=%SiteName%/%SiteAdmin% /p:AuthType=NTLM

ECHO Local deploying %SEQUOIA_ADMIN_PROJ% to %SiteName%/%SiteAdmin%
cd %AdminPackageFolderPath%
%SEQUOIA_ADMIN_PROJ%Pacakge-Release.deploy.cmd /Y /M:http://%ipaddr%/MsDeployAgentService /U:%username% /P:%password%

ECHO Exiting from preparing to deploy Sequoia.Admin