# A Python Client for Milvue API v3

This package allows to POST studies and GET results to/from Milvue API (https://milvue.com)

It implements STOW and WADO protocols from the DICOMweb Standard, https://www.dicomstandard.org/using/dicomweb

## Install 

```bash
pip install -e .
```

Create a `.env` file and define `MILVUE_API_URL` and `MILVUE_API_TOKEN`

## Example

See `scripts/predict_study.py`:

```python
import os
import sys
import pydicom
from pydicom.uid import generate_uid
import milvue_sdk
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("MILVUE_API_URL")
API_TOKEN = os.getenv("MILVUE_API_TOKEN")

# Load study dicoms + check all dicoms belong to the same study
dcm_list = [pydicom.dcmread(p) for p in sys.argv[1:]]

study_instance_uid = dcm_list[0].StudyInstanceUID
if any(dcm.StudyInstanceUID != study_instance_uid for dcm in dcm_list):
    raise Exception("All dicoms do not belong to the same study")

# Post study
milvue_sdk.post(API_URL, dcm_list, API_TOKEN)

# Wait for prediction
study_status = milvue_sdk.wait_done(API_URL, study_instance_uid, API_TOKEN)
if study_status["status"] != "done":
    raise RuntimeError("Prediction Error")

# Get Smarturgences results
smarturgences_dicoms = milvue_sdk.get(
    API_URL, study_instance_uid, "smarturgences", API_TOKEN
)
smarturgences_json = milvue_sdk.get_smarturgences(
    API_URL, study_instance_uid, API_TOKEN
)

# Get Smartxpert results
smartxpert_dicoms = milvue_sdk.get(API_URL, study_instance_uid, "smartxpert", API_TOKEN)
smartxpert_json = milvue_sdk.get_smartxpert(API_URL, study_instance_uid, API_TOKEN)
```

Usage:
```bash
python scripts/predict_study.py <path/to/dcm1> <path/to/dcm2>
```

## TODO

Implementation of dicom upload and download using signed urls instead of STOW/WADO

Implement post to `v3/interesting` route

Use Pydantic Schemas (generated with https://github.com/deepmap/oapi-codegen) describing JSON responses for non-DICOMweb routes:

- `GetStatusResponseV3`: schema for *v3/studies/{study_instance_uid}/status*, the current prediction status
- `GetSmarturgencesResponseV3`: schema for *v3/smarturgences/{study_instance_uid}*, Smarturgences results
- `GetSmartxpertResponseV3`: schema for *v3/smartxpert/{study_instance_uid}*, Smartxpert results


## Contact

Please write to contact@milvue.com for more information on Milvue integration
