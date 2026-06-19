@echo off
setlocal
REM ============================================================
REM  Nettoyage du deploiement manuel EN DOUBLE de gestion-agences
REM  dans WildFly. A lancer si erreur :
REM    WFLYSRV0205 ... Duplicate deployment ... will not be processed
REM
REM  ARRETEZ WildFly AVANT de lancer ce script.
REM
REM  Usage :
REM    clean-wildfly-deployment.bat  C:\chemin\vers\wildfly
REM  Exemple :
REM    clean-wildfly-deployment.bat  C:\wildfly-31.0.0.Final
REM ============================================================

if "%~1"=="" (
  echo.
  echo   Usage : clean-wildfly-deployment.bat ^<WILDFLY_HOME^>
  echo   Exemple : clean-wildfly-deployment.bat C:\wildfly-31.0.0.Final
  echo.
  exit /b 1
)

set "DEPLOY=%~1\standalone\deployments"
if not exist "%DEPLOY%" (
  echo   Dossier introuvable : %DEPLOY%
  echo   Verifiez le chemin de WildFly passe en parametre.
  exit /b 1
)

echo Nettoyage de : %DEPLOY%
for %%E in (war war.deployed war.dodeploy war.failed war.undeployed war.isdeploying) do (
  if exist "%DEPLOY%\gestion-agences-1.0-SNAPSHOT.%%E" (
    del /q "%DEPLOY%\gestion-agences-1.0-SNAPSHOT.%%E"
    echo   - supprime : gestion-agences-1.0-SNAPSHOT.%%E
  )
)

echo.
echo Termine. Redemarrez WildFly, puis deployez via IntelliJ UNIQUEMENT
echo (ne recopiez plus le WAR a la main dans deployments\).
endlocal
