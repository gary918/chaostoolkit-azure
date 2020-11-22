import os
import requests
from chaoslib import Configuration, Secrets
from logzero import logger


def get_cluster_status(secrets: Secrets = None, cluster_id=None) -> str:
    logger.debug(
        "Start get_cluster_status: cluster_id='{}'".format(
            cluster_id))

    response = requests.get(
        f"{secrets['url']}/api/2.0/clusters/get?cluster_id={cluster_id}",
        headers={"Authorization": f"Bearer {secrets['token']}"}
    )

    state = "N/A"
    if response.status_code == 200:
        state = response.json()['state']
    else:
        state = f"Error launching cluster: {response.json()['error_code']}: \
            {response.json()['message']}"

    return state


def cluster_exists(secrets: Secrets = None, cluster_name=None):
    logger.debug(
        "Start cluster_exists: cluster_name='{}'".format(
            cluster_name))

    response = requests.get(
        f"{secrets['url']}/api/2.0/clusters/list",
        headers={"Authorization": f"Bearer {secrets['token']}"}
    )

    exists = False
    if response.status_code == 200:
        if 'clusters' in response.json():
            clusters = response.json()['clusters']
            for cluster in clusters:
                if cluster['cluster_name'] == cluster_name:
                    exists = True
                    break
    else:
        logger.error(f"Error listing cluster: {response.json()['error_code']}: \
            {response.json()['message']}")

    return exists
