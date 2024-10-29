# Import necessary libraries
from google.cloud import bigquery
import oracledb
import pandas as pd

# Initialize BigQuery client
bq_client = bigquery.Client()

# Query the BigQuery table
query = "SELECT * FROM your_bigquery_table"
query_job = bq_client.query(query)

# Initialize Oracle connection
oracle_connection = oracledb.connect(user='your_user', password='your_password', dsn='your_dsn')
cursor = oracle_connection.cursor()

# Prepare insert statement
insert_sql = "INSERT INTO your_oracle_table (column1, column2, ...) VALUES (:1, :2, ...)"

# Batch size
batch_size = 5000

# Use an iterator to process results in batches
for batch in query_job.result(page_size=batch_size):  # Fetch results in pages
    # Convert batch to DataFrame
    df = pd.DataFrame(batch)
    print(df.columns)

    # Insert DataFrame into Oracle
    cursor.executemany(insert_sql, df.values.tolist())
    oracle_connection.commit()  # Commit the transaction

# Close the cursor and connection
cursor.close()
oracle_connection.close()
