import spotify
import requests
import base64
import pprint
import pandas as pd

cid='73592f8546db4e31ba2ccf2d809c45ad'
secret='391ff44f0d2749b79b7e344c90fde28a'

sp_client = spotify.Client(cid, secret)

sp_clients_creds=f"{cid}:{secret}"
sp_clients_creds_b64=base64.b64encode(sp_clients_creds.encode())

token_url="https://accounts.spotify.com/api/token"
method="POST"

token_data = {
    "grant_type": "client_credentials"
}

token_headers= {
    "Authorization": f"Basic {sp_clients_creds_b64.decode()}"
}

req = requests.post(token_url, data=token_data, headers=token_headers)
token_response_data = req.json()
access_token=token_response_data["access_token"]

print(access_token)


def get_podcasts_data(URI,search, type, market, offset, limit):
    '''Make an API request to Spotify API and returns a pandas dataframe'''
    
    id=[]
    name=[]
    description=[]
    total_episodes=[]

    query = f'{URI}'
    query += f'?q={search}'
    query +=f'&type={type}'
    query +=f'&market={market}'
    query += f'&offset={offset}'
    query += f'&limit={limit}'
    
    response = requests.get(url=query, headers={
        'Authorization': f'Bearer {access_token}'
    })

    json_res = response.json()

#    print(json_res)

    for el in range(len(json_res['shows']['items'])):
        name.append(json_res['shows']['items'][el]['name'])
        description.append(json_res['shows']['items'][el]['description'])
        id.append(json_res['shows']['items'][el]['id'])
        total_episodes.append(json_res['shows']['items'][el]['total_episodes'])

    df = pd.DataFrame()

    df['name'] = name  
    df['description']=description
    df['id']=id 
    df['total_episodes']=total_episodes

    print(df)

    return df 


