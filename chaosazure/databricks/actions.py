import random
import requests
from chaoslib import Secrets, Configuration
from chaoslib.exceptions import FailedActivity
from logzero import logger

from chaosazure import init_website_management_client
from chaosazure.common.resources.graph import fetch_resources
from chaosazure.webapp.constants import RES_TYPE_WEBAPP


__all__ = ["terminate_cluster", "start_cluster", "permanent_delete_cluster"]


def terminate_cluster(secrets: Secrets = None, cluster_id=None) -> int:
    logger.debug(
        "Start terminate_cluster: cluster_id='{}'".format(
            cluster_id))
    response = requests.post(
        f"{secrets['url']}/api/2.0/clusters/delete",
        headers={"Authorization": f"Bearer {secrets['token']}"},
        json={
          "cluster_id": cluster_id
        }
    )
    return response.status_code


def start_cluster(secrets: Secrets = None, cluster_id=None):
    logger.debug(
        "Start start_cluster: cluster_id='{}'".format(
            cluster_id))

    requests.post(
        f"{secrets['url']}/api/2.0/clusters/start",
        headers={"Authorization": f"Bearer {secrets['token']}"},
        json={
          "cluster_id": cluster_id
        }
    )


def get_cluster_id(secrets: Secrets = None, cluster_name=None):
    response = requests.get(
        f"{secrets['url']}/api/2.0/clusters/list",
        headers={"Authorization": f"Bearer {secrets['token']}"}
    )

    cluster_id = None
    if response.status_code == 200:
        if 'clusters' in response.json():
            clusters = response.json()['clusters']
            for cluster in clusters:
                if cluster['cluster_name'] == cluster_name:
                    cluster_id = cluster['cluster_id']
                    break

    if cluster_id is None:
        logger.error(f"Cluster_id for '{cluster_name}' not found")
    else:
        logger.debug(f"Get cluster_id={cluster_id}")

    return cluster_id


def permanent_delete_cluster(secrets: Secrets = None, cluster_name=None):
    logger.debug(
        "Start permanent_delete_cluster: cluster_name='{}'".format(
            cluster_name))

    cluster_id = get_cluster_id(secrets, cluster_name)
    response = requests.post(
        f"{secrets['url']}/api/2.0/clusters/permanent-delete",
        headers={"Authorization": f"Bearer {secrets['token']}"},
        json={
          "cluster_id": cluster_id
        }
    )
    logger.debug(response.json())


# Edit the cluster by changing the number of workers
def edit_cluster(secrets: Secrets = None, cluster_name=None, max_workers=8):
    logger.debug(
        f"Start edit_cluster: cluster_name='{cluster_name}', max_workers='{max_workers}'")

    cluster_id = get_cluster_id(secrets, cluster_name)
    response = requests.post(
        f"{secrets['url']}/api/2.0/clusters/edit",
        headers={"Authorization": f"Bearer {secrets['token']}"},
        json={
          "cluster_name": cluster_name,
          "cluster_id": cluster_id,
          "spark_version": "7.3.x-scala2.12",
          "node_type_id": "Standard_D3_v2",
          "autoscale": {
            "min_workers": 2,
            "max_workers": max_workers
          }
        }
    )
    logger.debug(response.json())
