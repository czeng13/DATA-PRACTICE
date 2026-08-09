import requests
from datetime import datetime

response = requests.get("https://api.github.com/rate_limit")

data = response.json()["resources"]["core"]

print("Remaining:", data["remaining"])
print("Reset time:", datetime.fromtimestamp(data["reset"]))