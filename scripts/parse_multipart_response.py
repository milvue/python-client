"""
python parse_multipart_response.py response_content.txt
"""

import sys
from io import BytesIO

import pydicom
from milvue_sdk.utils import decode_multipart


with open(sys.argv[1], "rb") as f:
    file_bytes = f.read()


dcm_list = decode_multipart(file_bytes, "multipart/related")

for dcm_bytes in dcm_list:
    dcm = pydicom.dcmread(BytesIO(dcm_bytes))
    name = f"{dcm.Modality}.{dcm.SOPInstanceUID}.dcm"
    dcm.save_as(name)
    print(name)
