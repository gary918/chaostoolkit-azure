import json
import requests
import sys


# Read the configuration
with open('config.json') as f:
    config = json.load(f)

secrets = config["secrets"]["databricks"]
cluster_name = config["configuration"]["cluster_name"]
job_id = config["configuration"]["job_id"]
notebook_path = config["configuration"]["notebook_path"]
cluster_id = None

# Create a new cluster
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
    print("Error creating cluster: %s: %s" % (response.json()["error_code"], response.json()["message"]))
    sys.exit("Error creating cluster")

# Reset the existing job by using the newly created cluster
cluster_id = response.json()["cluster_id"]
response = requests.post(
        f"{secrets['url']}/api/2.0/jobs/reset",
        headers={"Authorization": f"Bearer {secrets['token']}"},
        json={
            'job_id': job_id,
            'new_settings': {
              'name': 'test-job',
              'existing_cluster_id': cluster_id,
              'max_retries': -1,
              'notebook_task': {
                'notebook_path': notebook_path
              }, 
              'max_concurrent_runs': 1
            }
        }
    )

if response.status_code == 200:
    print(response.json())
else:
    print("Error resetting the job: %s: %s" % (response.json()["error_code"], response.json()["message"]))
    sys.exit("Error resetting the job")

# Run the job
response = requests.post(
        f"{secrets['url']}/api/2.0/jobs/run-now",
        headers={"Authorization": f"Bearer {secrets['token']}"},
        json={
          "job_id": job_id
        }
    )

if response.status_code == 200:
    print(response.json())
else:
    print("Error running the job: %s: %s" % (response.json()["error_code"], response.json()["message"]))
