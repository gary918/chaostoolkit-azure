import json
import requests

# curl -X GET -H "Authorization: Bearer [token]" https://[databricks url]/api/2.0/clusters/list

with open('config.json') as f:
    config = json.load(f)

secrets = config["secrets"]["databricks"]
cluster_name = config["configuration"]["cluster_name"]

response = requests.post(
        f"{secrets['url']}/api/2.0/clusters/create",
        headers={"Authorization": f"Bearer {secrets['token']}"},
        json={
          "cluster_name": cluster_name,
          "spark_version": "7.3.x-scala2.12",
          "node_type_id": "Standard_D3_v2",
          "autoscale": {
            "min_workers": 2,
            "max_workers": 8
          }
        }
    )

if response.status_code == 200:
    print(response.json())
else:
    print("Error launching cluster: %s: %s" % (response.json()["error_code"], response.json()["message"]))
