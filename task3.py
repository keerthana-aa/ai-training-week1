import hashlib
import hmac
import os

import requests
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "mysecret123")


response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)
response.raise_for_status()
users = response.json()

for user in users[:5]:
    print(f"{user['id']} - {user['name']} - {user['email']}")

first = users[0]
city = first["address"]["city"]
zip_code = first["address"].get("zipcode", "Not Available")
lat = first["address"]["geo"]["lat"]
company = first["company"]["name"]

print(f"City: {city} | Zip: {zip_code}")
print(f"Latitude: {lat} | Company: {company}")


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


payload = b'{"event": "order_created"}'
signature = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()

valid = verify_signature(payload, signature, WEBHOOK_SECRET)
tampered = verify_signature(b'{"event": "order_deleted"}', signature, WEBHOOK_SECRET)
wrong = verify_signature(payload, signature, "wrong_secret")

print(f"Valid: {valid} | Tampered: {tampered} | Wrong secret: {wrong}")
