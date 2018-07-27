set user_id=%1
set storage_type=%2

:: set storage_type=other
:: set storage_type=max
:: set storage_type=output

set username=%user_id%_%storage_type%
set password=%user_id%_123456
net user %username% %password% /add /y /fullname:"%username%" /comment:"aspera user of api" /passwordchg:no /expires:never 
WMIC USERACCOUNT WHERE "Name='%username%'" SET PasswordExpires=FALSE

