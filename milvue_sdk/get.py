import asyncio
import time

import pydicom
import requests

from .utils import decode_multipart


def wait_done(
    api_url, study_instance_uid, token, interval=3, timeout=180, verbose=False
):
    t1 = time.time() + timeout
    while time.time() < t1:
        study_status = get_status(api_url, study_instance_uid, token)
        if verbose:
            print(study_status)
        if study_status["status"] != "running":
            return study_status
        time.sleep(interval)
    return study_status


async def wait_done_async(
    api_url, study_instance_uid, token, interval=3, timeout=180, verbose=False
):
    t1 = time.time() + timeout
    while time.time() < t1:
        study_status = get_status(api_url, study_instance_uid, token)
        if verbose:
            print(study_status)
        if study_status["status"] != "running":
            return study_status
        await asyncio.sleep(interval)
    return study_status


def get_status(api_url: str, study_instance_uid: str, token: str):
    url = f"{api_url}/v3/studies/{study_instance_uid}/status"
    response = requests.get(url=url, headers={"x-goog-meta-owner": token})
    response.raise_for_status()
    return response.json()


def get(
    api_url: str,
    study_instance_uid: str,
    inference_command: str,
    token: str,
    **kwargs: dict,
) -> list[pydicom.Dataset]:
    url = f"{api_url}/v3/studies/{study_instance_uid}?inference_command={inference_command}&signed_url=False"
    query_string = "&".join([f"{k}={v}" for k, v in kwargs.items()])
    if query_string:
        url += f"&{query_string}"
    headers = {
        "content-type": "application/dicom",
        "x-goog-meta-owner": token,
    }
    response = requests.get(url=url, headers=headers)
    result = decode_multipart(response.content, response.headers.get("Content-Type"))
    return result


def get_signed_url():
    pass


def get_smarturgences(api_url: str, study_instance_uid: str, token: str):
    url = f"{api_url}/v3/smarturgences/{study_instance_uid}"
    response = requests.get(url=url, headers={"x-goog-meta-owner": token})
    response.raise_for_status()
    return response.json()


def get_smartxpert(api_url: str, study_instance_uid: str, token: str):
    url = f"{api_url}/v3/smartxpert/{study_instance_uid}"
    response = requests.get(url=url, headers={"x-goog-meta-owner": token})
    response.raise_for_status()
    return response.json()
