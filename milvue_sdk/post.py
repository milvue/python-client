import pydicom
from utils import write_dataset_to_bytes, encode_multipart
import requests


def post(
    api_url: str, dcm_list: list[pydicom.Dataset], token: str, params: dict = {}
) -> requests.Response:
    url = f"{api_url}/v3/studies?signed_url=False"
    part_list = []
    for dcm in dcm_list:
        part = write_dataset_to_bytes(dcm)
        part_list.append((part, "application/dicom"))
    body, content_type = encode_multipart(json_field=params, bytes_fields=part_list)
    headers = {"Content-Type": content_type, "x-goog-meta-owner": token}
    r = requests.post(url, data=body, headers=headers)
    r.raise_for_status()
    return r


def post_signed_url():
    raise NotImplementedError


def post_interesting():
    raise NotImplementedError
