@ECHO OFF
ECHO Checking if web application folder exists
SET SEQUOIA_WEBROOT=C:\Sequoia
SET SEQUOIA_CLIQSTUDIOS_WEBFOLDER=%SEQUOIA_WEBROOT%\Sequoia.CliqStudios
SET SEQUOIA_SHARED_WEBFOLDER=%SEQUOIA_WEBROOT%\Sequoia.Shared
SET SEQUOIA_CLIQWS_WEBFOLDER=%SEQUOIA_WEBROOT%\Sequoia.AsyncWS
SET SEQUOIA_ADMIN_WEBFOLDER=%SEQUOIA_WEBROOT%\Sequoia.Admin
SET SiteName=cliqtest
SET Websvc=cliqws
SET SiteAdmin=admin
REM SET AppFolderPath=%SEQUOIA_WEBROOT%\Sequoia.CliqStudios
SET appcmd=CALL %WINDIR%\system32\inetsrv\appcmd
SET ipaddr=172.30.9.19
SET port=80
SET sslport=443
SET websvcport=7001

IF EXIST %SEQUOIA_WEBROOT% (
	ECHO %SEQUOIA_WEBROOT% folder exists
) ELSE (
	ECHO Creating %SEQUOIA_WEBROOT% folder
	MD %SEQUOIA_WEBROOT%
)
IF EXIST %SEQUOIA_CLIQSTUDIOS_WEBFOLDER% (
	ECHO %SEQUOIA_CLIQSTUDIOS_WEBFOLDER% folder exists
) ELSE (
	ECHO Creating %SEQUOIA_CLIQSTUDIOS_WEBFOLDER% folder
	MD %SEQUOIA_CLIQSTUDIOS_WEBFOLDER%
)
IF EXIST %SEQUOIA_SHARED_WEBFOLDER% (
	ECHO %SEQUOIA_SHARED_WEBFOLDER% folder exists
) ELSE (
	ECHO Creating %SEQUOIA_SHARED_WEBFOLDER% folder
	MD %SEQUOIA_SHARED_WEBFOLDER%
)
IF EXIST %SEQUOIA_CLIQWS_WEBFOLDER% (
	ECHO %SEQUOIA_CLIQWS_WEBFOLDER% folder exists
) ELSE (
	ECHO Creating %SEQUOIA_CLIQWS_WEBFOLDER% folder
	MD %SEQUOIA_CLIQWS_WEBFOLDER%
)
IF EXIST %SEQUOIA_ADMIN_WEBFOLDER% (
	ECHO %SEQUOIA_ADMIN_WEBFOLDER% folder exists
) ELSE (
	ECHO Creating %SEQUOIA_ADMIN_WEBFOLDER% folder
	MD %SEQUOIA_ADMIN_WEBFOLDER%
)

ECHO Creating/Updating %SiteName% site on IIS
%appcmd% list site / %SiteName%
IF "%ERRORLEVEL%" EQU "0" (
    ECHO Site %SiteName% exists
    ECHO Update config, setting if needed
) ELSE (
    ECHO Site %SiteName% does not exist
    ECHO Creating site %SiteName%  
    %appcmd% add site -name:%SiteName% -physicalPath:%SEQUOIA_CLIQSTUDIOS_WEBFOLDER% 
)

ECHO Creating/Updating %Websvc% site on IIS
%appcmd% list site / %Websvc%
IF "%ERRORLEVEL%" EQU "0" (
    ECHO Site %Websvc% exists
    ECHO Update config, setting if needed
) ELSE (
    ECHO Site %Websvc% does not exist
    ECHO Creating site %Websvc%  
    %appcmd% add site -name:%Websvc% -physicalPath:%SEQUOIA_CLIQWS_WEBFOLDER% 
)

ECHO Creating/Updating %SiteAdmin% of %SiteName% site on IIS
%appcmd% list app %SiteName%/%SiteAdmin%/ | findstr /R ?*%SiteAdmin%
IF "%ERRORLEVEL%" EQU "0" (
    ECHO %SiteAdmin% webapp already exists in %SiteName% site
) ELSE (
    ECHO Site %SiteAdmin% does not exist in %SiteName%
    ECHO Creating webapp %SitAdmin% in %SiteName% site
    %appcmd% add app -site.name:%SiteName% -path:/%SiteAdmin% -physicalPath:%SEQUOIA_ADMIN_WEBFOLDER% 
)

ECHO Creating/Updating %SiteName%_apppool of application pool on IIS
%appcmd% list apppool / %SiteName%_apppool
IF "%ERRORLEVEL%" EQU "0" (
    ECHO %SiteName%_appPool exists
    ECHO Assigning application pool %SiteName%_apppool to %SiteName% site
    %appcmd%  set app -app.name:%SiteName%/ -applicationPool:%SiteName%_apppool 

    ECHO Assigning application pool %SiteName%_apppool to %Websvc% site
    %appcmd% set app -app.name:%Websvc%/ -applicationPool:%SiteName%_apppool 

    ECHO Assigning application pool %SiteName%_apppool to %SiteName%/%SiteAdmin% webapp
    %appcmd% set app -app.name:%SiteName%/%SiteAdmin% -applicationPool:%SiteName%_apppool 

) ELSE (
    ECHO %SiteName%_appPool does not exist
    ECHO Creating application pool %SiteName%_AppPool
    %appcmd% add apppool -name:%SiteName%_apppool -managedRuntimeVersion:v4.0 -managedPipelineMode:Classic -processModel.identityType:NetworkService

    ECHO Assigning application pool %SiteName%_apppool to site %SiteName%
    %appcmd%  set app -app.name:%SiteName%/ -applicationPool:%SiteName%_apppool  

    ECHO Assigning application pool %SiteName%_apppool to site %Websvc%
    %appcmd%  set app -app.name:%Websvc%/ -applicationPool:%SiteName%_apppool 

    ECHO Assigning application pool %SiteName%_apppool to %SiteName%/%SiteAdmin% webapp
    %appcmd% set app -app.name:%SiteName%/%SiteAdmin% -applicationPool:%SiteName%_apppool 
)

ECHO Binding HTTP to %SiteName% of IIS
%appcmd% list site %SiteName% | findstr /r http/[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*:%port%
IF "%ERRORLEVEL%" EQU "0" ( 
    ECHO HTTP port %port% has already bond to %SiteName%
    
) ELSE (
    ECHO HTTP port %port% has not bind to %SiteName% yet
    ECHO Binding HTTP port %port% to %SiteName% 
    %appcmd% set site -site.name:%SiteName% -+bindings.[protocol='http',bindingInformation='%ipaddr%:%port%:']
)

ECHO Binding HTTP to %Websvc% of IIS
%appcmd% list site %Websvc% | findstr /r http/[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*:%websvcport%
IF "%ERRORLEVEL%" EQU "0" ( 
    ECHO HTTP port %websvcport% has already bond to %WebSvc%
    
) ELSE (
    ECHO HTTP port %websvcport% has not bind to %WebSvc% yet
    ECHO Binding HTTP port %websvcport% to %WebSvc% 
    %appcmd% set site -site.name:%WebSvc% -+bindings.[protocol='http',bindingInformation='%ipaddr%:%websvcport%:']
    rem VERIFY > nul
    rem exit /b 0
    rem ver > nul  
)

%appcmd% list site  %SiteName% | findstr /R Stopped
IF "%ERRORLEVEL%" EQU "0" (
    ECHO  %SiteName% has already started
) ELSE (
   ECHO  %SiteName% has stopped
   ECHO Starting website %SiteName%...
   %appcmd% start site -site.name:%SiteName% 
)
%appcmd% list site  %Websvc% | findstr /R Stopped
IF "%ERRORLEVEL%" EQU "0" (
    ECHO  %Websvc% has already started
) ELSE (
   ECHO  %Websvc% has stopped
   ECHO Starting website %Websvc%...
   %appcmd% start site -site.name:%Websvc%
   REM VERIFY > nul
   REM exit /b 0
   REM ver > nul  
   
)
ECHO Before performing Powershell scripts 