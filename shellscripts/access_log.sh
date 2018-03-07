#!/bin/sh

#Fetch contents from apache log files
log_file=$1

echo -e "Top 10 IP addresses which accessed the website \n"

less $log_file | awk {'print $1'} | grep . | sort | uniq -c | sort -nr | head -10

echo -e "Top 10 URLs browsed \n"

less $log_file | awk {'print $7'} | grep . | sort | uniq -c | sort -nr | head -10

echo -e "IP addresses accessed the site from '07/Mar/2004:16:06:51' to '07/Mar/2004:20:55:43' \n"

sed -n '/07\/Mar\/2004:16:06:51/,/07\/Mar\/2004:20:55:43/p' $1 | awk {'print $1'}|grep . | sort | uniq -c | sort -nr
