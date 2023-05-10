
from google.cloud import bigquery

# Create BigQuery client 
client=bigquery.Client()

def read_data_to_df(query):
    '''Executes a query in BigQuery table and returns a pandas dataframe'''
    res = client.query(query)

    df = res.to_dataframe()
    print(df)
    return df 


def load_data_from_df(table_id, df, schema):
    '''Gets a pandas dataframe and loads the data into BigQuery table'''
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition="WRITE_TRUNCATE" # replaces data
    )

    job = client.load_table_from_dataframe(
        df, 
        table_id, 
        job_config=job_config
    )

    job.result()   




