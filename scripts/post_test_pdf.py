import requests
import sys
url = 'http://127.0.0.1:8002/redact/pdf'
files = {'file': open('test.pdf','rb')}
try:
    r = requests.post(url, files=files, timeout=15)
    print('status:', r.status_code)
    print('headers:')
    for k,v in r.headers.items():
        print(k+':', v)
    # if JSON error
    ctype = r.headers.get('Content-Type','')
    if 'application/json' in ctype:
        print('json body:', r.text)
    else:
        with open('redacted_test.pdf','wb') as f:
            f.write(r.content)
        print('wrote redacted_test.pdf,', len(r.content), 'bytes')
except Exception as e:
    print('error', e)
    sys.exit(1)
