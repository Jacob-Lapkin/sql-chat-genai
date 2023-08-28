from google.cloud import bigquery as bq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re

client = bq.Client()

def query_bigquery(query):
    query_job = client.query(
        query
    )

    results = query_job.result()  # Waits for job to complete.
    data = []
    for row in results:
        data.append(row)

    return data


def query_bigquery_w_wc(query):
    data = query_bigquery(query)
    total_words = 0

    for row in data:
        for column in row.values():
            if isinstance(column, str):
                words = re.findall(r'\w+', column)
                total_words += len(words)

    print('Estimated total word count:', total_words)
    print("-"*30)

    return data


def get_table_schema(project, dataset, table):
    table = client.get_table(f'{project}.{dataset}.{table}')
    return table.schema

# print(get_table_schema("imgcp-20220210133450", "PIMCOREPROD", "DESCRIPTION"))

def query_bigquery_sql(query):
    query_job = client.query(query)
    results = query_job.result()  # Waits for job to complete.
    df = results.to_dataframe()
    return df

def get_example_row(project, dataset, table):
    query_job = client.query(f'SELECT * FROM `{project}.{dataset}.{table}` LIMIT 1')
    results = query_job.result()  # Waits for job to complete.
    df = results.to_dataframe()

    return df

