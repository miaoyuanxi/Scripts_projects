set user_id=%1
set user_others_input_pathname_root=%2
set user_max_input_pathname_root=%3
set user_output_pathname_root=%4

:: set user_id=1846853
:: set user_others_input_pathname_root=\\10.60.100.101\d\inputdata5
:: set user_max_input_pathname_root=\\10.60.100.102\d\inputdata5
:: set user_output_pathname_root=\\10.60.100.201\d\outputdata5

set /a temp_id=((%user_id% - (%user_id% %% 500) ) * 500 / 500)
set user_sub_path=%temp_id%\%user_id%
set user_others_input_pathname=%user_others_input_pathname_root%\%user_sub_path%
set user_max_input_pathname=%user_max_input_pathname_root%\%user_sub_path%
set user_output_pathname=%user_output_pathname_root%\%user_sub_path%

set username=%user_id%_other
set password=%user_id%_123456
set docroot=%user_others_input_pathname%
net user %username% %password% /add /y /fullname:"%username%" /comment:"aspera user of api" /passwordchg:no /expires:never 
WMIC USERACCOUNT WHERE "Name='%username%'" SET PasswordExpires=FALSE

if exist "c:\Program Files (x86)\Aspera\Enterprise Server\bin\asconfigurator.exe" ("C:\Program Files (x86)\Aspera\Enterprise Server\bin\asconfigurator.exe" -x set_user_data;user_name,%username%;absolute,%docroot%
"C:\Program Files (x86)\Aspera\Enterprise Server\bin\asconfigurator.exe" -x set_user_data;user_name,%username%;docroot_mask,%docroot%;read_allowed,true
"C:\Program Files (x86)\Aspera\Enterprise Server\bin\asconfigurator.exe" -x set_user_data;user_name,%username%;docroot_mask,%docroot%;write_allowed,true
)

set username=%user_id%_max
set password=%user_id%_123456
set docroot=%user_max_input_pathname%
net user %username% %password% /add /y /fullname:"%username%" /comment:"aspera user of api" /passwordchg:no /expires:never 
WMIC USERACCOUNT WHERE "Name='%username%'" SET PasswordExpires=FALSE

if exist "c:\Program Files (x86)\Aspera\Enterprise Server\bin\asconfigurator.exe" ("C:\Program Files (x86)\Aspera\Enterprise Server\bin\asconfigurator.exe" -x set_user_data;user_name,%username%;absolute,%docroot%
"C:\Program Files (x86)\Aspera\Enterprise Server\bin\asconfigurator.exe" -x set_user_data;user_name,%username%;docroot_mask,%docroot%;read_allowed,true
"C:\Program Files (x86)\Aspera\Enterprise Server\bin\asconfigurator.exe" -x set_user_data;user_name,%username%;docroot_mask,%docroot%;write_allowed,true
)

set username=%user_id%_output
set password=%user_id%_123456
set docroot=%user_output_pathname%
net user %username% %password% /add /y /fullname:"%username%" /comment:"aspera user of api" /passwordchg:no /expires:never 
WMIC USERACCOUNT WHERE "Name='%username%'" SET PasswordExpires=FALSE

if exist "c:\Program Files (x86)\Aspera\Enterprise Server\bin\asconfigurator.exe" ("C:\Program Files (x86)\Aspera\Enterprise Server\bin\asconfigurator.exe" -x set_user_data;user_name,%username%;absolute,%docroot%
"C:\Program Files (x86)\Aspera\Enterprise Server\bin\asconfigurator.exe" -x set_user_data;user_name,%username%;docroot_mask,%docroot%;read_allowed,true
"C:\Program Files (x86)\Aspera\Enterprise Server\bin\asconfigurator.exe" -x set_user_data;user_name,%username%;docroot_mask,%docroot%;write_allowed,true
)
