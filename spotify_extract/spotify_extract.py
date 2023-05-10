import os
import requests
from google.cloud import bigquery
import pandas as pd
from utils.bigquery_handler import client, read_data_to_df, load_data_from_df
from utils.spotify_api_handler import sp_client, get_podcasts_data
#from dotenv import load_dotenv

#load_dotenv()

################### Get first 50 results of query search "Data Hackers"

# Search params 
SPOTIFY_URI ="https://api.spotify.com/v1/search"
QUERY = 'Data+Hackers'
TYPE="show"
MARKET='ES'
OFFSET="0"
LIMIT="50"

podcast_df = get_podcasts_data(SPOTIFY_URI, QUERY, TYPE, MARKET, OFFSET, LIMIT)

################### 




################### Store results in BigQuery

TABLE_PODCASTS_ID='case-gb-2.spotify_data.podcast'
TABLE_DATA_HACKERS_GB='case-gb-2.spotify_data.data_hackers_gb'
TABLE_DATA_HACKERS='case-gb-2.spotify_data.data_hackers_episodes'

#table_id=f"{PROJECT_ID}.{bg_dataset}.{table_name}"

schema_podcasts=[
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("description", "STRING"),
    bigquery.SchemaField("id", "STRING"),
    bigquery.SchemaField("total_episodes", "INTEGER")
]

schema_data_hackers=[
    bigquery.SchemaField("id", "INTEGER"),
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("description", "STRING"),
    bigquery.SchemaField("release_date", "DATE"),
    bigquery.SchemaField("duration_ms", "STRING"),
    bigquery.SchemaField("language", "STRING"),
    bigquery.SchemaField("explicit", "STRING"),
    bigquery.SchemaField("type", "STRING"),

]

load_data_from_df(TABLE_PODCASTS_ID, podcast_df, schema_podcasts)

pod_query="""
    SELECT * 
    FROM spotify_data.podcast
    LIMIT 10
"""

read_data_to_df(pod_query)