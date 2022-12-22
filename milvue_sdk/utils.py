from typing import Tuple
import gzip
from io import BytesIO

import pydicom
import requests
from pydicom.filebase import DicomFileLike
from requests_toolbelt import MultipartDecoder, MultipartEncoder


def write_dataset_to_bytes(dcm, **kwargs):
    with BytesIO() as buffer:
        memory_dataset = DicomFileLike(buffer)
        write_like_original = kwargs.get("write_like_original", False)
        pydicom.dcmwrite(memory_dataset, dcm, write_like_original=write_like_original)
        # to read from the object, you have to rewind it
        memory_dataset.seek(0)
        return memory_dataset.read()


def encode_multipart(
    part: bytes,
    content_type: str,
    boundary=None,
    encoding="utf-8",
) -> Tuple[str, str]:
    fields = [("elem_0", ("elem_0", part, content_type))]
    encoder = MultipartEncoder(fields, boundary=boundary, encoding=encoding)
    return encoder.to_string(), f"multipart/related; boundary={encoder.boundary_value}"


def decode_multipart(r: requests.Response) -> list[bytes]:
    if len(r.content) == 38:  # b'--32LongBoundary--\r\n': empty response
        return []
    decoder = MultipartDecoder(
        content=r.content,
        content_type=r.headers.get("Content-Type"),
        encoding="utf-8",
    )
    dicom_bytes_list = []
    for part in decoder.parts:
        part_content_type = part.headers.get(b"Content-Type")
        if part_content_type == b"application/dicom":
            dicom_bytes_list.append(part.content)
        if part_content_type == b"application/dicom+gzip":
            dicom_bytes_list.append(gzip.decompress(part.content))
    return dicom_bytes_list
