import os
import sys
import json
import requests

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
        sessionid = config['sessionid']
        authorization = config['authorization']
        presentation_id = config['presentation_id']
except:
    print('Error: config.json not found or invalid.')
    sys.exit()

headers = {
    'authorization': authorization,
    'cookie'       : f'sessionid={sessionid}',
    'user-agent'   : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

response = requests.get(f'https://pro.yuketang.cn/api/v3/lesson/presentation/fetch?presentation_id={presentation_id}', headers=headers)
if response.status_code != 200:
    print(f'Error: {response.status_code}')
    sys.exit()
response = response.json()
if response['code'] != 0:
    print(f'Error: {response["message"]}')
    sys.exit()

os.makedirs('problems', exist_ok=True)

slides = response['data']['slides']
for slide in slides:
    try:
        problem = slide['problem']
        response = requests.get(f'{slide['cover']}', headers=headers)
        if response.status_code != 200:
            print(f'Error: {response.status_code}')
            sys.exit()
        with open(f'problems/Slide_{slide['index']}.jpg', 'wb') as f:
            f.write(response.content)
    except:
        pass
print('Done.')