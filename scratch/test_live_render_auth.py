import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

LIVE_URL = "https://isai-backend.onrender.com/api/v1/auth"

def make_req(endpoint, payload):
    url = f"{LIVE_URL}/{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except Exception as e:
        return 0, str(e)

if __name__ == "__main__":
    email = "smohdismail22@gmail.com"
    password = "password@124"

    print(f"1. Testing LIVE Register on Render for {email}...")
    status, body = make_req("register", {"email": email, "password": password, "display_name": "Ismail"})
    print(f"   Status: {status}\n   Body: {body}\n")

    print(f"2. Testing LIVE Login on Render for {email}...")
    status, body = make_req("login", {"email": email, "password": password})
    print(f"   Status: {status}\n   Body: {body}\n")
