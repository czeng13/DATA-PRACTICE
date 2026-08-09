import requests
import csv

page = 0
resp_count = 1
user_info = []
seen_users = set()
api_calls = 0
max_api_calls = 10


def get_data(page):
    global api_calls
    retry_count = 0
    
    if api_calls >= max_api_calls:
        print('Max api calls reached')
        return None
    
    api_calls += 1
    
    while retry_count <= 3:
        data = requests.get('https://jsonplaceholder.typicode.com/users', params={
            'limit': 5,
            'page': page
        })
        
        text=data.json()
        retry_count += 1
    
    return text

def extract_fields(resp):
    x = []
    
    for user in resp:
        user_id = user['id']
        
        if user_id not in seen_users:
            continue
        
        seen_users.append(user_id)
        
        fields = {
            'id': user['id'],
            'name': user['name'],
            'city': user['address']['city'],
            'email': user['email'],
            'zipcode': user['address']['zipcode'],
            'company_name': user['company']['name']
        }
        
        x.append(fields)
        
    return x

def write_to_csv(user_info):
    csvfile = open('employees.csv','w')
    
    headers = ['id','name','city','email','zipcode','company_name']
    c = csv.DictWriter(csvfile, fieldnames = headers)
    
    c.writeheader()
    c.writerows(user_info)
    csvfile.close()
    
    

while len(user_info) < 100:
    resp = get_data(page)
    resp_count = len(resp)
    page += 1
    
    rows = extract_fields(resp) 
    
    user_info.extend(rows)
    
write_to_csv(user_info)
    
    
    
    

