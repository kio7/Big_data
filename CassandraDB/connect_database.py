from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

with open('big_data-token.json', "r") as f:
    creds = json.load(f)
    ASTRA_DB_APPLICATION_TOKEN = creds["token"]

cluster = Cluster(
    cloud={
        "secure_connect_bundle": 'secure-connect-big-data.zip',
    },
    auth_provider=PlainTextAuthProvider(
        "token",
        ASTRA_DB_APPLICATION_TOKEN,
    ),
)

session = cluster.connect('sag_netflix')

# row = session.execute("select release_version from system.local").one()
# if row:
#     print(row[0])
# else:
#     print("An error occurred.")