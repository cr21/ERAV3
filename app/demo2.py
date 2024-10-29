# Import necessary libraries
from google.cloud import bigquery
import oracledb

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
batch = []

# Use an iterator to process results in batches
for row in query_job.result(page_size=batch_size):  # Fetch results in pages
    batch.append(tuple(row))  # Convert row to tuple for insertion

    # If batch size is reached, execute the insert
    if len(batch) == batch_size:
        cursor.executemany(insert_sql, batch)
        oracle_connection.commit()  # Commit the transaction
        batch = []  # Reset batch

# Insert any remaining records in the last batch
if batch:
    cursor.executemany(insert_sql, batch)
    oracle_connection.commit()

# Close the cursor and connection
cursor.close()
oracle_connection.close()
