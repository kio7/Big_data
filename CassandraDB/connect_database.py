from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import os

file_path = os.path.abspath(os.path.dirname(__file__))

with open(file_path + '/big_data-token.json', "r") as f:
    creds = json.load(f)
    ASTRA_DB_APPLICATION_TOKEN = creds["token"]

cluster = Cluster(
    cloud={
        "secure_connect_bundle": file_path + '/secure-connect-big-data.zip',
    },
    auth_provider=PlainTextAuthProvider(
        "token",
        ASTRA_DB_APPLICATION_TOKEN,
    ),
)

c_session = cluster.connect('bigdata3and4')

# row = session.execute("select release_version from system.local").one()
# if row:
#     print(row[0])
# else:
#     print("An error occurred.")