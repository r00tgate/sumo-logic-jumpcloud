
#!/usr/bin/python
import datetime
import pytz
import requests
import json

#set this to the https endpoint you've created for SumoLogic ingestion
sumourl = 'https://endpoint[#].collection.[us].sumologic.com/receiver/v1/http/[FULL URI]'

#set this to the jumpdrive API URL
jumpcloudapiurl = 'https://events.jumpcloud.com/events'

#set this to your jumpdrive API key
apikey = '[INSERT API KEY '

#set this to the number of minutes in the past (relative to runtime) that you want to start log retrieval
minutesdelta = 5


#get current time
endtime = datetime.datetime.utcnow()
endtime = endtime.replace(tzinfo=pytz.UTC)

#try to read the the starttime from file (i.e. the endtime from the last run). If this fails set the starttime to timedelta minutes in the past
try:
        with open("/opt/jumpcloud-log-collector-jumpcloudlastaccess.txt", 'r') as datefile:
                starttimestr = datefile.read()

except:
        starttime = endtime - datetime.timedelta(minutes=minutesdelta)
        starttime = starttime.replace(tzinfo=pytz.UTC)
        # starttimestr = starttime.replace(microsecond=0).isoformat("T")+"Z"
        starttimestr = starttime.strftime("%Y-%m-%dT%H:%M:%SZ")



# endtimestr = endtime.replace(microsecond=0).isoformat("T")+"Z"
endtimestr = endtime.strftime("%Y-%m-%dT%H:%M:%SZ")


payload = "startDate=" + starttimestr + "&" + "endDate=" + endtimestr
headers = {
    'x-api-key': apikey,
    'content-type': "application/json",
    }
print headers
print payload

#try to retrieve the logs and update push them to SumoLogic
try:

        response = requests.request("GET", jumpcloudapiurl, params=payload, headers=headers)
        print response
        data = json.loads(response.text)
        for line in data:
                line = json.dumps(line)
                post = requests.post(sumourl, data = line)
                print line
        with open("/opt/jumpcloud-log-collector/jumpcloudlastaccess.txt", 'w') as datefile:
                datefile.write(endtimestr)

except Exception as e:

        print "Something didn't work."

