; Instalator programu Shank po polsku (Inno Setup 6). Budowanie: tools\zbuduj_instalator.py
; Pliki do spakowania przygotowuje skrypt budujacy w folderze PAKIET (przekazywany przez /DPAKIET=...).

#define Nazwa "Shank po polsku"
#ifndef Wersja
  #define Wersja "1.0"
#endif
#ifndef PAKIET
  #define PAKIET "D:\ShankPolski-audio\pakiet"
#endif

[Setup]
AppId={{6B0E2A4C-7F1D-4C8E-9B3A-5D2F8E1C4A70}
AppName={#Nazwa}
AppVersion={#Wersja}
AppVerName={#Nazwa} {#Wersja}
AppPublisher=Projekt fanowski
DefaultDirName={autopf}\{#Nazwa}
DefaultGroupName={#Nazwa}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=..\dist
OutputBaseFilename=ShankPoPolsku-{#Wersja}-instalator
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayName={#Nazwa}
UninstallDisplayIcon={app}\{#Nazwa}.exe
CloseApplications=no

[Languages]
Name: "pl"; MessagesFile: "compiler:Languages\Polish.isl"

[Tasks]
Name: "autostart"; Description: "Uruchamiaj program w tle razem z Windows (zalecane)"
Name: "pulpit"; Description: "Skrót na Pulpicie (uruchamia program i grę)"

[Files]
Source: "{#PAKIET}\*"; DestDir: "{app}"; Excludes: "shank_polski.ini"; Flags: ignoreversion recursesubdirs createallsubdirs
; ustawienia gracza zostaja przy aktualizacji
Source: "{#PAKIET}\shank_polski.ini"; DestDir: "{app}"; Flags: onlyifdoesntexist

[InstallDelete]
; stare nagrania z poprzedniej wersji
Type: filesandordirs; Name: "{app}\lektor"
Type: filesandordirs; Name: "{app}\napisy"

[Icons]
Name: "{group}\{#Nazwa}"; Filename: "{app}\{#Nazwa}.exe"; Comment: "Uruchamia program i grę Shank"
Name: "{group}\Ustawienia"; Filename: "notepad.exe"; Parameters: """{app}\shank_polski.ini"""
Name: "{group}\Czytaj mnie"; Filename: "notepad.exe"; Parameters: """{app}\CZYTAJ_MNIE.txt"""
Name: "{group}\Folder programu"; Filename: "{app}"
Name: "{group}\Odinstaluj {#Nazwa}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#Nazwa}"; Filename: "{app}\{#Nazwa}.exe"; Tasks: pulpit
Name: "{userstartup}\{#Nazwa} w tle"; Filename: "{app}\{#Nazwa}.exe"; Parameters: "--w-tle"; Tasks: autostart

[Run]
Filename: "{app}\{#Nazwa}.exe"; Parameters: "--w-tle"; Flags: nowait; Description: "Uruchom program w tle"
Filename: "notepad.exe"; Parameters: """{app}\CZYTAJ_MNIE.txt"""; Flags: postinstall nowait skipifsilent unchecked; Description: "Pokaż instrukcję"

[UninstallRun]
Filename: "{sys}\taskkill.exe"; Parameters: "/F /IM ""{#Nazwa}.exe"""; Flags: runhidden; RunOnceId: "Zatrzymaj"

[UninstallDelete]
Type: files; Name: "{app}\shank_polski.log"

[Code]
// Dzialajacy w tle program blokuje swoje pliki: zatrzymac go przed kopiowaniem.
function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  Kod: Integer;
begin
  Exec(ExpandConstant('{sys}\taskkill.exe'), '/F /IM "{#Nazwa}.exe"', '', SW_HIDE, ewWaitUntilTerminated, Kod);
  Sleep(500);
  Result := '';
end;
