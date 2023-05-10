import spotify
import requests
import base64
import pandas as pd

cid='73592f8546db4e31ba2ccf2d809c45ad'
secret='391ff44f0d2749b79b7e344c90fde28a'

sp_client = spotify.Client(cid, secret)

def authenticate():
    '''Make an API request to Spotify API 
    and returns an access token for authentication'''

    sp_clients_creds=f"{cid}:{secret}"
    sp_clients_creds_b64=base64.b64encode(sp_clients_creds.encode())

    token_url="https://accounts.spotify.com/api/token"

    token_data = {
        "grant_type": "client_credentials"
    }

    token_headers= {
        "Authorization": f"Basic {sp_clients_creds_b64.decode()}"
    }

    req = requests.post(token_url, data=token_data, headers=token_headers)
    token_response_data = req.json()
    access_token=token_response_data["access_token"]
    # print(access_token)

    return access_token


def get_podcasts_data(URI,search, type, market, offset, limit):
    '''Make an API request to Spotify API 
    and returns a pandas dataframe'''
    
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
    
    access_token=authenticate()
    response = requests.get(url=query, headers={
        'Authorization': f'Bearer {access_token}'
    })

    json_res = response.json()

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

    n_rows = len(df)
    print(f"Created a dataframe with {n_rows} rows")

    return df 

def get_episodes_data(URI,show_id,market, offset, limit):
    '''Make an API request to Spotify API 
    to get all episodes from a podcast 
    and returns a pandas dataframe'''
    
    id=[]
    name=[]
    description=[]
    release_date=[]
    duration_ms=[]
    language=[]
    explicit=[]
    type=[]


    query = f'{URI}'
    query += f'/{show_id}/episodes?'
    query += f'offset={offset}'
    query +=f'&market={market}'
    query += f'&limit={limit}'

    access_token=authenticate()
    response = requests.get(url=query, headers={
        'Authorization': f'Bearer {access_token}'
    })

    json_res = response.json()

    for el in range(len(json_res['items'])):
        id.append(json_res['items'][el]['id'])
        name.append(json_res['items'][el]['name'])
        description.append(json_res['items'][el]['description'])
        release_date.append(json_res['items'][el]['release_date'])
        duration_ms.append(json_res['items'][el]['duration_ms'])
        language.append(json_res['items'][el]['language'])
        explicit.append(json_res['items'][el]['explicit'])
        type.append(json_res['items'][el]['type'])


    df = pd.DataFrame()
    
    df['id']=id
    df['name'] = name  
    df['description']=description
    df['release_date']=release_date
    df['duration_ms']=duration_ms
    df['language']=language
    df['explicit']=explicit 
    df['type']=type  

    n_rows = len(df)
    print(f"Created a dataframe with {n_rows} rows")

    return df 

def filter_episodes(df, query):

    '''Filter a pandas dataframe by column value'''
    filtered_df = df.loc[df['name'].str.contains(query, case=False)] 
    
    n_rows = len(filtered_df)
    print(f"Created a dataframe with {n_rows} rows")

    return filtered_df