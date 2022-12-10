import datetime
import json

import requests
import urllib3

import em

urllib3.disable_warnings()

s = requests.session()
s.headers = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28'
}

target_events = []
columns = ['Actor', 'Repo', 'Time']

src = s.get('https://api.github.com/users/qhy040404/received_events', verify=False).text
src_json: dict = json.loads(src)

outdated_time = datetime.datetime.utcnow() - datetime.timedelta(days=1)
print('Outdated time: ' + outdated_time.strftime('%Y-%m-%d %H:%M:%S'))

event: dict
for event in src_json:
    if event['type'] == 'WatchEvent':
        latest = datetime.datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        if latest > outdated_time:
            target_events.append([
                event['actor']['login'],
                event['repo']['name'],
                event['created_at']
            ])

if len(target_events) > 0:
    print(str(len(target_events)) + ' events')
    em.send_email(target_events, columns)
else:
    print('No update.')
