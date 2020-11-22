import json
import requests

with open('config.json') as f:
  config = json.load(f)

secrets = config["secrets"]["databricks"]
cluster_name = config["configuration"]["cluster_name"]

""" response = requests.get(
  f'https://{DOMAIN}/api/2.0/clusters/list',
  headers={'Authorization': 'Bearer %s' % TOKEN}
)

response = requests.get(
  f'https://{DOMAIN}/api/2.0/clusters/get?cluster_id={cluster_id}',
  headers={'Authorization': 'Bearer %s' % TOKEN}
)

response = requests.get(
  f'https://{DOMAIN}/api/2.0/clusters/list',
  headers={'Authorization': 'Bearer %s' % TOKEN}
)

response = requests.post(
        f"{secrets['url']}/api/2.0/clusters/start",
        headers={"Authorization": f"Bearer {secrets['token']}"},
        json={
          "cluster_id": cluster_id
        }
    )

response = requests.post(
        f"{secrets['url']}/api/2.0/clusters/delete",
        headers={"Authorization": f"Bearer {secrets['token']}"},
        json={
          "cluster_id": cluster_id
        }
    )

response = requests.post(
        f"{secrets['url']}/api/2.0/clusters/permanent-delete",
        headers={"Authorization": f"Bearer {secrets['token']}"},
        json={
          "cluster_id": cluster_id
        }
    )

response = requests.post(
        f"{secrets['url']}/api/2.0/clusters/create",
        headers={"Authorization": f"Bearer {secrets['token']}"},
        json={
          "cluster_name": "test-cluster",
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
  if 'clusters' in response.json():
    clusters = response.json()['clusters']
    for cluster in clusters:
      if cluster['cluster_name'] == 'test-cluster':
        print(cluster['cluster_id'])
  else:
    print('no')
else:
  print(response.status_code)
  print("Error launching cluster: %s: %s" % (response.json()["error_code"], response.json()["message"])) """


response = requests.get(
        f"{secrets['url']}/api/2.0/jobs/list",
        headers={"Authorization": f"Bearer {secrets['token']}"}
    )

if response.status_code == 200:
  print(response.json())
else:
  print(response.status_code)
  print("Error launching cluster: %s: %s" % (response.json()["error_code"], response.json()["message"]))


""" response = requests.post(
        f"{secrets['url']}/api/2.0/jobs/reset",
        headers={"Authorization": f"Bearer {secrets['token']}"},
        json={
            'job_id': 1, 
            'new_settings': {
              'name': 'test-job', 
              'existing_cluster_id': '1117-015038-half649', 
              'email_notifications': {}, 
              'timeout_seconds': 600, 
              'max_retries': -1, 
              'min_retry_interval_millis': 10000, 
              'retry_on_timeout': True, 
              'notebook_task': {
                'notebook_path': '/Users/ganwa@microsoft.com/test'
              }, 
              'max_concurrent_runs': 1
            }
        }
    ) """
response = requests.get(
        # f"{secrets['url']}/api/2.0/jobs/runs/get-output?run_id=930",
        f"{secrets['url']}/api/2.0/jobs/runs/list?job_id=1&active_only=true",
        headers={"Authorization": f"Bearer {secrets['token']}"}
    )

if response.status_code == 200:
  print(response.json())
else:
  print(response.status_code)
  print("Error launching cluster: %s: %s" % (response.json()["error_code"], response.json()["message"]))
# curl -X GET -H "Authorization: Bearer <PAT>" <DATABRICKS_URL>
