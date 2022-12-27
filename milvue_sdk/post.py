import pydicom
import requests

from .utils import encode_multipart, write_dataset_to_bytes


async def post(
    api_url: str, dcm_list: list[pydicom.Dataset], token: str, params: dict = {}
) -> requests.Response:
    url = f"{api_url}/v3/studies?signed_url=False"
    bytes_list = []
    for dcm in dcm_list:
        bytes_list.append(write_dataset_to_bytes(dcm))
    body, content_type = encode_multipart(bytes_list)
    headers = {"Content-Type": content_type, "x-goog-meta-owner": token}
    r = requests.post(url, data=body, headers=headers)
    r.raise_for_status()
    return r


async def post_signed_url():
    raise NotImplementedError


async def post_interesting():
    raise NotImplementedError
