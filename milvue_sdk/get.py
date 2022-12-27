import asyncio
import time

import pydicom
import requests

from .utils import decode_multipart


async def wait_done(
    api_url, study_instance_uid, token, interval=3, timeout=180, verbose=False
):
    t1 = time.time() + timeout
    while time.time() < t1:
        study_status = await get_status(api_url, study_instance_uid, token)
        if verbose:
            print(study_status)
        if study_status["status"] != "running":
            return study_status
        await asyncio.sleep(interval)
    return study_status


async def get_status(api_url: str, study_instance_uid: str, token: str):
    url = f"{api_url}/v3/studies/{study_instance_uid}/status"
    r = requests.get(url=url, headers={"x-goog-meta-owner": token})
    r.raise_for_status()
    return r.json()


async def get(
    api_url: str,
    study_instance_uid: str,
    inference_command: str,
    token: str,
) -> list[pydicom.Dataset]:
    url = f"{api_url}/v3/studies/{study_instance_uid}?inference_command={inference_command}&signed_url=False"
    headers = {
        "content-type": "application/dicom",
        "x-goog-meta-owner": token,
    }
    r = requests.get(url=url, headers=headers)
    res = decode_multipart(r.content, r.headers.get("Content-Type"))
    return res


def get_signed_url():
    pass


async def get_smarturgences(api_url: str, study_instance_uid: str, token: str):
    url = f"{api_url}/v3/smarturgences/{study_instance_uid}"
    r = requests.get(url=url, header={"x-goog-meta-owner": token})
    r.raise_for_status()
    return r.json()


async def get_smartxpert(api_url: str, study_instance_uid: str, token: str):
    url = f"{api_url}/v3/smartxpert/{study_instance_uid}"
    r = requests.get(url=url, header={"x-goog-meta-owner": token})
    r.raise_for_status()
    return r.json()
