@ECHO OFF
ECHO Preparing to deploy Sequoia.Shared
SET SiteName=cliqtest
SET appcmd=CALL %WINDIR%\system32\inetsrv\appcmd
SET SEQUOIA_SHARED_PROJ=Sequoia.Shared
SET VDIR=Shared
SET SourceFolderPath=C:\Jenkins_Git_Repositiry\SequoiaWebSite\Sequoia.Shared
SET TargetFolderPath=C:\Sequoia\Sequoia.Shared
SET ipaddr=172.30.9.19
SET username=jenkins
SET password=P@ssw0rd123

ECHO Deploying shared resources of %SEQUOIA_SHARED_PROJ% to target virtual directory %SiteName%/%VDIR%

REM cd %SourceFolderPath%
REM ECHO Building %SEQUOIA_SHARED_PROJ% as web-package 
REM msbuild %SEQUOIA_SHARED_PROJ%.csproj /p:DeployOnBuild=true /p:Configuration=Release;PackageLocation=%SEQUOIA_SHARED_PROJ%Pacakge-Release.zip /P:DeployIISAppPath=%SiteName%/%VDIR% /p:AuthType=NTLM



REM ECHO Local deploying %SEQUOIA_SHARED_PROJ% to %SiteName%/%SEQUOIA_SHARED_PROJ%
REM cd %SourceFolderPath%
REM %SEQUOIA_SHARED_PROJ%Pacakge-Release.deploy.cmd /Y /M:http://%ipaddr%/MsDeployAgentService /U:%username% /P:%password%

cd %SourceFolderPath%
ECHO Local deploying %SEQUOIA_SHARED_PROJ% to virtual directory %SiteName%/%SEQUOIA_SHARED_PROJ%

"C:\Program Files (x86)\IIS\Microsoft Web Deploy V3\msdeploy.exe" -verb:sync -source:contentPath=%SourceFolderPath% -dest:contentPath=%TargetFolderPath%

%appcmd% list vdir %SiteName%/%VDIR%/ | findstr /R %VDIR%
IF "%ERRORLEVEL%" EQU "0" (
    ECHO virtual directory %VDIR% already exists in %SiteName% site
       
) ELSE (
    ECHO Creating virtual directory %VDIR% of %SiteName% site
    %appcmd% add vdir -app.name:%SiteName%/ -path:/%VDIR% -physicalPath:%TargetFolderPath%
)

ECHO Starting %SiteName%...
%appcmd% list site  %SiteName% | findstr /R Stopped
IF "%ERRORLEVEL%" EQU "0" (
    
   ECHO  %SiteName% has stopped
   ECHO Starting site %SiteName% 
   %appcmd% start site -site.name:%SiteName%
   
) ELSE (
   ECHO  %SiteName% has already started
   VERIFY > nul
   exit /b 0
   ver > nul  
   
)
ECHO Exiting from preparing to deploy Sequoia.Shared