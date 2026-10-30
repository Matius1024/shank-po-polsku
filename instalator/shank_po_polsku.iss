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
AppPublisherURL=https://github.com/Matius1024/shank-po-polsku
AppUpdatesURL=https://github.com/Matius1024/shank-po-polsku/releases/latest
VersionInfoVersion={#Wersja}
VersionInfoDescription=Instalator programu {#Nazwa}
DefaultDirName={autopf}\{#Nazwa}
DefaultGroupName={#Nazwa}
DisableProgramGroupPage=yes
; mniej stron do przejscia z czytnikiem ekranu
DisableReadyPage=yes
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
; opcja odznaczona przy aktualizacji: usunac skrot z poprzedniej instalacji
Type: files; Name: "{userstartup}\{#Nazwa} w tle.lnk"; Tasks: not autostart
Type: files; Name: "{autodesktop}\{#Nazwa}.lnk"; Tasks: not pulpit

[Icons]
Name: "{group}\{#Nazwa}"; Filename: "{app}\{#Nazwa}.exe"; Comment: "Uruchamia program i grę Shank"
Name: "{group}\Ustawienia"; Filename: "notepad.exe"; Parameters: """{app}\shank_polski.ini"""
Name: "{group}\Czytaj mnie"; Filename: "notepad.exe"; Parameters: """{app}\CZYTAJ_MNIE.txt"""
Name: "{group}\Folder programu"; Filename: "{app}"
Name: "{group}\Odinstaluj {#Nazwa}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#Nazwa}"; Filename: "{app}\{#Nazwa}.exe"; Tasks: pulpit
Name: "{userstartup}\{#Nazwa} w tle"; Filename: "{app}\{#Nazwa}.exe"; Parameters: "--w-tle"; Tasks: autostart

[Run]
Filename: "{app}\{#Nazwa}.exe"; Parameters: "--w-tle"; Flags: nowait; Tasks: autostart
Filename: "notepad.exe"; Parameters: """{app}\CZYTAJ_MNIE.txt"""; Flags: postinstall nowait skipifsilent unchecked; Description: "Pokaż instrukcję"

[UninstallRun]
Filename: "{sys}\taskkill.exe"; Parameters: "/F /IM ""{#Nazwa}.exe"""; Flags: runhidden; RunOnceId: "Zatrzymaj"

[UninstallDelete]
Type: files; Name: "{app}\shank_polski.log"

[Code]
var
  StronaFolderu: TInputDirWizardPage;
  Manifest: String;

// Plik Steam o zainstalowanej grze (app 6120): w glownym folderze Steam albo w innej bibliotece.
function ZnajdzManifest(var Wynik: String): Boolean;
var
  Steam, Linia: String;
  Linie: TArrayOfString;
  I: Integer;
begin
  Result := False;
  if not RegQueryStringValue(HKCU, 'Software\Valve\Steam', 'SteamPath', Steam) then
    Exit;
  StringChangeEx(Steam, '/', '\', True);
  Wynik := Steam + '\steamapps\appmanifest_6120.acf';
  if FileExists(Wynik) then
  begin
    Result := True;
    Exit;
  end;
  if not LoadStringsFromFile(Steam + '\steamapps\libraryfolders.vdf', Linie) then
    Exit;
  for I := 0 to GetArrayLength(Linie) - 1 do
  begin
    Linia := Trim(Linie[I]);
    if Pos('"path"', Lowercase(Linia)) = 1 then
    begin
      Linia := Trim(Copy(Linia, 7, Length(Linia)));
      Linia := Copy(Linia, 2, Length(Linia) - 2);
      StringChangeEx(Linia, '\\', '\', True);
      Wynik := Linia + '\steamapps\appmanifest_6120.acf';
      if FileExists(Wynik) then
      begin
        Result := True;
        Exit;
      end;
    end;
  end;
end;

function GalazClassic: Boolean;
var
  Linie: TArrayOfString;
  I: Integer;
begin
  Result := False;
  if LoadStringsFromFile(Manifest, Linie) then
    for I := 0 to GetArrayLength(Linie) - 1 do
      if (Pos('"BetaKey"', Linie[I]) > 0) and (Pos('"classic"', Linie[I]) > 0) then
        Result := True;
end;

function FolderGryUstawiony: Boolean;
begin
  Result := Trim(GetIniString('ustawienia', 'folder_gry', '', ExpandConstant('{app}\shank_polski.ini'))) <> '';
end;

procedure InitializeWizard;
begin
  StronaFolderu := CreateInputDirPage(wpSelectTasks, 'Folder gry',
    'Nie znaleziono gry Shank na Steam.',
    'Jeśli masz grę z innego źródła, na przykład GOG, wpisz jej folder. Możesz też zostawić puste pole i przejść dalej.',
    False, '');
  StronaFolderu.Add('Folder gry Shank (można zostawić puste):');
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := (PageID = StronaFolderu.ID) and ((Manifest <> '') or FolderGryUstawiony);
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  Folder: String;
begin
  Result := True;
  if CurPageID = StronaFolderu.ID then
  begin
    Folder := Trim(StronaFolderu.Values[0]);
    if (Folder <> '') and not FileExists(Folder + '\Shank.exe') and not FileExists(Folder + '\bin\Shank.exe') then
    begin
      MsgBox('W tym folderze nie ma gry: brak pliku Shank.exe. Popraw folder albo zostaw puste pole.', mbError, MB_OK);
      Result := False;
    end;
  end;
end;

// Wpisuje folder gry do ustawien; plik w UTF-8, bo tak czyta go program.
procedure ZapiszFolderGry(Folder: String);
var
  Plik: String;
  Linie: TArrayOfString;
  I: Integer;
begin
  Plik := ExpandConstant('{app}\shank_polski.ini');
  if not LoadStringsFromFile(Plik, Linie) then
    Exit;
  for I := 0 to GetArrayLength(Linie) - 1 do
    if Pos('folder_gry=', Linie[I]) = 1 then
      Linie[I] := 'folder_gry=' + Folder;
  SaveStringsToUTF8File(Plik, Linie, False);
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  Folder: String;
begin
  if CurStep <> ssPostInstall then
    Exit;
  Folder := Trim(StronaFolderu.Values[0]);
  if Folder <> '' then
    ZapiszFolderGry(Folder);
  // Komunikat, nie napis na stronie: czytnik ekranu przeczyta go na pewno.
  if (Manifest <> '') and not GalazClassic then
    SuppressibleMsgBox('Gra Shank jest w zwykłej wersji. Program działa, ale część scenek będzie mieć tylko lektora, bez audiodeskrypcji.' + #13#10 + #13#10 +
      'Aby mieć audiodeskrypcję we wszystkich scenkach, włącz gałąź classic: w Steam kliknij prawym przyciskiem grę Shank, wybierz Właściwości, potem Wersje beta i z listy wybierz classic.',
      mbInformation, MB_OK, IDOK);
end;

function InitializeSetup: Boolean;
begin
  if not ZnajdzManifest(Manifest) then
    Manifest := '';
  Log('Gra na Steam: ' + Manifest);
  if Manifest <> '' then
    Log('Galaz classic: ' + IntToStr(Ord(GalazClassic)));
  Result := True;
end;

// Dzialajacy w tle program blokuje swoje pliki: zatrzymac go przed kopiowaniem.
function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  Kod: Integer;
begin
  Exec(ExpandConstant('{sys}\taskkill.exe'), '/F /IM "{#Nazwa}.exe"', '', SW_HIDE, ewWaitUntilTerminated, Kod);
  Sleep(500);
  Result := '';
end;
