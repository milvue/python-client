from typing import Tuple
import gzip
from io import BytesIO

import pydicom
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
    bytes_list: list[bytes],
    content_type: str = "application/dicom",
    boundary=None,
    encoding="utf-8",
) -> Tuple[str, str]:

    fields = [
        (f"elem_{i}", (f"elem_{i}", x, content_type)) for i, x in enumerate(bytes_list)
    ]
    encoder = MultipartEncoder(fields, boundary=boundary, encoding=encoding)
    return encoder.to_string(), f"multipart/related; boundary={encoder.boundary_value}"


def decode_multipart(content, content_type) -> list[bytes]:
    if len(content) == 38:  # b'--32LongBoundary--\r\n': empty response
        return []
    decoder = MultipartDecoder(
        content=content,
        content_type=content_type,
        encoding="utf-8",
    )
    dcm_list = []
    for part in decoder.parts:
        part_content_type = part.headers.get(b"Content-Type")
        if part_content_type == b"application/dicom":
            dcm_bytes = part.content
        elif part_content_type == b"application/dicom+gzip":
            dcm_bytes = gzip.decompress(part.content)
        else:
            continue
        dcm = pydicom.dcmread(BytesIO(dcm_bytes))
        dcm_list.append(dcm)
    return dcm_list
