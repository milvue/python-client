import pydicom
from utils import decode_multipart
import requests
from milvueapi import (
    InferenceCommandEnum,
    GetStudyStatusResponseV3,
    GetSmarturgencesResponseV3,
    GetSmartxpertResponseV3,
)


def wait_done():
    raise NotImplementedError


def get_status(
    api_url: str, study_instance_uid: str, token: str
) -> GetStudyStatusResponseV3:
    url = f"{api_url}/v3/studies/{study_instance_uid}/status"
    r = requests.get(url=url, header={"x-goog-meta-owner": token})
    r.raise_for_status()
    res = GetStudyStatusResponseV3(**r.json())
    return res


def get(
    api_url: str,
    study_instance_uid: str,
    inference_command: InferenceCommandEnum,
    token: str,
) -> list[pydicom.Dataset]:
    url = f"{api_url}/v3/studies/{study_instance_uid}?inference_command={inference_command}&signed_url=False"
    headers = {
        "content-type": "application/dicom",
        "x-goog-meta-owner": token,
    }
    r = requests.get(url=url, header=headers)
    res = decode_multipart(r.content, r.headers.get("Content-Type"))
    return res


def get_signed_url():
    pass


def get_smarturgences(
    api_url: str, study_instance_uid: str, token: str
) -> GetSmarturgencesResponseV3:
    url = f"{api_url}/v3/smarturgences/{study_instance_uid}"
    r = requests.get(url=url, header={"x-goog-meta-owner": token})
    r.raise_for_status()
    res = GetSmarturgencesResponseV3(**r.json())
    return res


def get_smartxpert(
    api_url: str, study_instance_uid: str, token: str
) -> GetSmartxpertResponseV3:
    url = f"{api_url}/v3/smartxpert/{study_instance_uid}"
    r = requests.get(url=url, header={"x-goog-meta-owner": token})
    r.raise_for_status()
    res = GetSmartxpertResponseV3(**r.json())
    return res
