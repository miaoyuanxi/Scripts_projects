set CLASSPATH=%CLASSPATH%;  
set PATH=%PATH%  
set JAVA_HOME=%JAVA_HOME%
C:
cd C:\apache-flume-1.8.0-bin\bin
@echo "开始执行flume 采集程序"
flume-ng.cmd agent -conf ../conf -conf-file ../conf/flume-kafka.properties --name foo -property flume.root.logger=INFO,LOGFILE