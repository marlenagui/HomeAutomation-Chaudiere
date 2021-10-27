[TOC]

# PYTHON
## list of useful commands to run from python prompt
```
from nap.url import Url
from configParser import read_config
configFile = 'config.ini'
arestioConfig = read_config(configFile, 'arestio')
consignesConfig = read_config(configFile, 'consignes')
digitalIOConfig = read_config(configFile, 'digitalIO')
urlPath = 'digital/' + digitalIOConfig['relais_vanne'][1] + "/0"
print(urlPath)
urlApi = 'http://' + arestioConfig['api_url'] + ':' + arestioConfig['api_url_port'] + '/'
print(urlApi)```

---

# MYSQL
## Help created DB schema and permissions
http://zetcode.com/db/mysqlpython/

## list of useful commands to run from mysql prompt
```
mysql.exe -u root -p -h 192.168.1.3
show databases;
use log;
select from_unixtime(date), severity, text from log where from_unixtime(date) like '2016-11-22%' and function like 'VANNE%';
```


## Create event in mysql to run query at define time
lots about event here : http://www.mysqltutorial.org/mysql-triggers/working-mysql-scheduled-event/

1. set event scheduler on
```
SET GLOBAL event_scheduler = ON;```
2. unset safe update mode, safe update mode prevent to alter without providing key
```
SET SQL_SAFE_UPDATES = 0;```
3. create the event
```
CREATE EVENT AutoDeleteOldlogs
ON SCHEDULE AT CURRENT_TIMESTAMP + interval 1 DAY
ON COMPLETION PRESERVE
DO
DELETE LOW_PRIORITY FROM maison.log WHERE date < unix_timestamp(DATE_SUB(now(), INTERVAL 10 DAY));
```

## list all the events
```
show processlist;```
## Delete an event
```
DROP EVENT AutoDeleteOldlogs;```



