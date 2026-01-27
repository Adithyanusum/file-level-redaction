import requests, json, time
import numpy as np
import cv2

BASE = 'http://127.0.0.1:8000'

# create sample image
img = np.full((200,300,3), 255, dtype=np.uint8)
cv2.putText(img, 'SECRET', (30,110), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)
cv2.imwrite('sample.png', img)
print('Wrote sample.png')

# wait a bit for server
print('Waiting 1s for server...')
time.sleep(1)

# signup
s = requests.Session()
try:
    r = s.post(BASE + '/signup', json={'username':'tester','password':'pass'})
    if r.status_code == 400 and 'user exists' in r.text:
        print('user exists, will login')
        r = s.post(BASE + '/login', json={'username':'tester','password':'pass'})
    token = r.json().get('token')
    print('Got token')
except Exception as e:
    print('Signup/login failed', e)
    raise

headers = {'Authorization': 'Bearer ' + token}
regions = [[30,60,200,60]]
files = {'file': ('sample.png', open('sample.png','rb'), 'image/png')}
data = {'regions': json.dumps(regions), 'mode': 'blackout'}
print('Uploading for redaction...')
r = s.post(BASE + '/redact/image', files=files, data=data, headers=headers)
if r.status_code == 200:
    open('out_sample.png','wb').write(r.content)
    print('Wrote out_sample.png')
else:
    print('Redaction failed', r.status_code, r.text)
