@echo off

echo cleark...

FORFILES /p d:\enfwork /D -3  /C "cmd /c  if @isdir=="TRUE" echo dont close Is cleaning enfwork @file&rd /Q /S @path"
FORFILES /p d:\log /D -7  /C "cmd /c  if @isdir=="TRUE" echo dont close Is cleaning log @file&rd /Q /S @path"
FORFILES /p c:\enfuzion\temp /D -7  /C "cmd /c  if @isdir=="FALSE" echo dont close Is cleaning enfuzion temp @file&del /Q @path"