import os
import socket
import requests
import json

threshold = 95
#test-alerts channel webhook
WEBHOOK_URL = "https://hooks.slack.com/services/vhhgsckasisscnjiogfhbwndl"
#slack channel
slackchannel = "#production_alerts"

def check_disk():
    """Function to find disk usage"""

    disk_stat = {}
    partitions = os.popen("df -h | egrep -vw 'devtmpfs|tmpfs|Filesystem' | awk {'print $NF'}").read()

    for i in partitions.split('\n'):
        if i:
            command = "df -h | grep -w '%s'| awk {'print $5'} | cut -d '%s' -f1" % (i, '%')
            disk_free = int(os.popen(command).read().strip('\n'))
            if disk_free >= threshold:
                disk_stat[i] = disk_free
    return disk_stat

def slack_notification(message, attachments):

    payload = {
        'text': "*" + message + "*",
        'channel': slackchannel,
        'username': 'Stage-watchman',
        'icon_emoji': ':fire:'}
    if attachments:
        payload['attachments'] = attachments
    r = requests.post(WEBHOOK_URL, data=json.dumps(payload),
                      headers={'Content-Type': 'application/json'})
    return r.status_code

if __name__ == "__main__":

    hostname = socket.gethostname()
    alert_dict = check_disk()
    if len(alert_dict.keys()) != 0:

        message = "CRTICAL: Disk space is critical on %s" %(hostname)
        body = ""
        for i in alert_dict.keys():
            body += "%s - partition is %s%s used\n" % (i, alert_dict[i], '%')
        attachments = [{
            'color': 'danger',
            'fields': [{
                'title': 'Details',
		'value': body
            }]
        }]
        slack_notification(message, attachments)