#!/bin/sh
ps -ef | grep gestionChaudiere | grep -vE "grep|color" 
pids=`ps -ef | grep gestionChaudiere | grep -vE "color|grep" | awk '{ print $2 }'`
echo $pids
for pid in ${pids}
do
	echo "kill -9 ${pid}"
	kill -9 ${pid}
done
curl http://192.168.1.4:8088/digital/4/1
curl http://192.168.1.4:8088/digital/5/1
curl http://192.168.1.4:8088/digital/6/1
curl http://192.168.1.4:8088/digital/7/1
