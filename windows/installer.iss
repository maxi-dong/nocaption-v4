; ============================================================================
; installer.iss – Inno Setup script for NOCAPTION V4
; Compile with Inno Setup 6+  (https://jrsoftware.org/isinfo.php)
; ============================================================================

#define MyAppName      "NOCAPTION V4"
#define MyAppVersion   "4.0.0"
#define MyAppPublisher "NOCAPTION"
#define MyAppExeName   "NOCAPTION V4.exe"

[Setup]
; Basic metadata
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

; Output
OutputDir=installer_output
OutputBaseFilename=NOCAPTION_V4_Setup

; Compression (lzma2/ultra64 for best ratio)
Compression=lzma2/ultra64
SolidCompression=yes

; 64-bit only
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Modern wizard
WizardStyle=modern

; No license page required
LicenseFile=
InfoBeforeFile=

; Privileges – install per-user by default, can elevate
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Uninstaller
Uninstallable=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

; Misc
DisableProgramGroupPage=yes
SetupIconFile=icon.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Bundle everything from the PyInstaller one-folder output
Source: "dist\NOCAPTION V4\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start-menu shortcut
Name: "{group}\{#MyAppName}";        Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
; Desktop shortcut (optional task)
Name: "{autodesktop}\{#MyAppName}";  Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Offer to launch after install
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
