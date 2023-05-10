from google.cloud import bigquery
from utils.bigquery_handler import read_data_to_df, load_data_from_df
from utils.spotify_api_handler import get_podcasts_data, get_episodes_data
from dotenv import load_dotenv

load_dotenv()

# Initialize params  
SPOTIFY_SEARCH_URI ="https://api.spotify.com/v1/search"
QUERY = 'Data+Hackers'
TYPE="show"
MARKET='ES'
OFFSET="0"
LIMIT="50"

SPOTIFY_SHOW_URI ="https://api.spotify.com/v1/shows"  
ID="1oMIHOXsrLFENAeM743g93" # Data Hackers https://open.spotify.com/show/1oMIHOXsrLFENAeM743g93?si=eb986ffafa204bd6

TABLE_PODCASTS_ID='case-gb-2.spotify_data.podcast' # table_id=f"{PROJECT_ID}.{bg_dataset}.{table_name}"
TABLE_DATA_HACKERS_GB='case-gb-2.spotify_data.data_hackers_gb'
TABLE_DATA_HACKERS='case-gb-2.spotify_data.data_hackers_eps'

SCHEMA_PODCASTS=[
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("description", "STRING"),
    bigquery.SchemaField("id", "STRING"),
    bigquery.SchemaField("total_episodes", "INTEGER")
]

SCHEMA_DATA_HACKERS=[
    bigquery.SchemaField("id", "STRING"),
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("description", "STRING"),
    bigquery.SchemaField("release_date", "STRING"),
    bigquery.SchemaField("duration_ms", "INTEGER"),
    bigquery.SchemaField("language", "STRING"),
    bigquery.SchemaField("explicit", "BOOLEAN"),
    bigquery.SchemaField("type", "STRING")
]

################### Get first 50 results of query search "Data Hackers"

podcast_df = get_podcasts_data(SPOTIFY_SEARCH_URI, QUERY, TYPE, MARKET, OFFSET, LIMIT)

################### Get Data Hackers Episodes

eps_podcast_df = get_episodes_data(SPOTIFY_SHOW_URI, ID, MARKET, OFFSET,LIMIT)



load_data_from_df(TABLE_PODCASTS_ID, podcast_df, SCHEMA_PODCASTS)
# load_data_from_df(TABLE_DATA_HACKERS, eps_podcast_df, SCHEMA_DATA_HACKERS)



pod_query="""
    SELECT * 
    FROM spotify_data.data_hackers_eps
    LIMIT 10
"""

read_data_to_df(pod_query)