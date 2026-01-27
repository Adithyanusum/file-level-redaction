from fastapi.testclient import TestClient
from app.main import app
import numpy as np
import cv2
import json

client = TestClient(app)

# create sample image
img = np.full((200,300,3), 255, dtype=np.uint8)
cv2.putText(img, 'SECRET', (30,110), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)
cv2.imwrite('sample.png', img)
print('Wrote sample.png')

# signup
r = client.post('/signup', json={'username':'tester2','password':'pass'})
if r.status_code == 200:
    token = r.json()['token']
    print('Signup OK')
else:
    print('Signup failed', r.status_code, r.text)
    # try login
    r2 = client.post('/login', json={'username':'tester2','password':'pass'})
    token = r2.json().get('token')
    print('Login OK')

headers = {'Authorization': 'Bearer ' + token}
regions = [[30,60,200,60]]
files = {'file': ('sample.png', open('sample.png','rb'), 'image/png')}
data = {'regions': json.dumps(regions), 'mode': 'blackout'}
print('Uploading for redaction...')
r = client.post('/redact/image', files=files, data=data, headers=headers)
if r.status_code == 200:
    open('out_sample.png','wb').write(r.content)
    print('Wrote out_sample.png')
else:
    print('Redaction failed', r.status_code, r.text)
