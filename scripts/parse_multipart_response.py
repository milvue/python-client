"""
python parse_multipart_response.py response_content.txt
"""

import sys
from io import BytesIO

from milvue_sdk.utils import decode_multipart


with open(sys.argv[1], "rb") as f:
    file_bytes = f.read()

boundary = file_bytes[2:34].decode()
content_type = f"multipart/related; boundary={boundary}"

dcm_list = decode_multipart(file_bytes, content_type)
for dcm in dcm_list:
    name = f"{dcm.Modality}.{dcm.SOPInstanceUID}.dcm"
    dcm.save_as(name)
    print(name)
