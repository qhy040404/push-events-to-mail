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

event: dict
for event in src_json:
    if event['type'] == 'WatchEvent':
        target_events.append([
            event['actor']['login'],
            event['repo']['name'],
            event['created_at']
        ])

em.send_email(target_events, columns)
