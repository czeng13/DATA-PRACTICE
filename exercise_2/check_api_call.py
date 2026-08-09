import requests

response = requests.get(
    "https://api.github.com/orgs/microsoft/repos",
    params={
        "per_page": 1,
        "page": 1
    }
)

print("Status:", response.status_code)
print("Headers:", response.headers)
print("Response:", response.json())