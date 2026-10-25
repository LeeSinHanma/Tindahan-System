#ifndef AppVersion
  #define AppVersion "0.1.0"
#endif

[Setup]
AppId={{622914F8-84DA-4759-B96D-28F71C682E2D}
AppName=Tindahan System
AppVersion={#AppVersion}
DefaultDirName={localappdata}\Programs\TindahanSystem
DefaultGroupName=Tindahan System
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir=..\..\dist\releases
OutputBaseFilename=Tindahan-System-{#AppVersion}-windows-x86_64-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\POS-System.exe
CloseApplications=yes
SetupLogging=yes

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked

[Files]
Source: "..\..\dist\POS-System\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Tindahan System"; Filename: "{app}\POS-System.exe"
Name: "{autodesktop}\Tindahan System"; Filename: "{app}\POS-System.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\POS-System.exe"; Description: "Launch Tindahan System"; Flags: nowait postinstall skipifsilent

; Shop data lives outside {app} and is intentionally retained on uninstall.
