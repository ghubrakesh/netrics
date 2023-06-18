[Setup]
AppName=Netrics
AppVersion=1.0
DefaultDirName={pf}\Netrics
DefaultGroupName=Netrics
OutputDir=.
OutputBaseFilename=NetricsSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\Netrics.exe"; DestDir: "{app}"
Source: "logo.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\Netrics"; Filename: "{app}\Netrics.exe"; IconFilename: "{app}\logo.ico"

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "Netrics"; ValueData: "{app}\Netrics.exe"; Flags: uninsdeletevalue

[Code]
var
  AppMutex: string;

function InitializeSetup(): Boolean;
begin
  AppMutex := 'Netrics_' + ExpandConstant('{#emit SetupSetting("AppVersion")}');
  Result := True;
end;
