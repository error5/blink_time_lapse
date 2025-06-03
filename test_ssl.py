import ssl
import urllib.request

import certifi

print("Using cert bundle:", certifi.where())
url = "https://rest-prod.immedia-semi.com/"

context = ssl.create_default_context(cafile=certifi.where())

try:
    with urllib.request.urlopen(url, context=context) as response:
        print("✅ SSL connection successful")
except Exception as e:
    print("❌ SSL connection failed:", e)
