# A Python Client for Milvue API v3

This package allows to POST studies and GET results to/from Milvue API (https://milvue.com)

It implements STOW and WADO protocols from the DICOMweb Standard, https://www.dicomstandard.org/using/dicomweb

## Install 

```bash
pip install -e .
```

## Example

```python
import pydicom

import milvue_sdk

# Define api url and token
API_URL = ""
API_TOKEN = ""

# Study to process
DICOM_PATHS = ["/path/to/dicom1", "path/to/dicom2"]
dcm_list = [pydicom.dcmread(p) for p in DICOM_PATHS]
study_instance_uid = dcm_list[0].StudyInstanceUID

# Check all dicoms belong to the same study
for dcm in dcm_list[1:]:
    assert dcm.StudyInstanceUID == study_instance_uid

milvue_sdk.post(API_URL, dicom_list, API_TOKEN)
study_status = await milvue_sdk.wait_done(
    API_URL, dcm.StudyInstanceUID, API_TOKEN
)
if study_status["status"] != "done":
    raise RuntimeError("Prediction Error")

# Get Smarturgences results
smarturgences_dicoms = milvue_sdk.get(
    API_URL, study_instance_uid, "smarturgences", API_TOKEN
)
smarturgences_json = milvue_sdk.get_smarturgences(API_URL, study_instance_uid, API_TOKEN)

# Get Smartxpert results
smartxpert_dicoms = milvue_sdk.get(
    API_URL, study_instance_uid, "smartxpert", API_TOKEN
)
smartxpert_json = milvue_sdk.get_smartxpert(API_URL, study_instance_uid, API_TOKEN)
```


TODO:

Implementation of dicom upload and download using signed urls instead of STOW/WADO

In addition, the following Pydantic Schemas (generated with https://github.com/deepmap/oapi-codegen) describe JSON responses for non-DICOMweb routes:

- `GetStatusResponseV3`: schema for *v3/studies/{study_instance_uid}/status*, the current prediction status
- `GetSmarturgencesResponseV3`: schema for *v3/smarturgences/{study_instance_uid}*, Smarturgences results
- `GetSmartxpertResponseV3`: schema for *v3/smartxpert/{study_instance_uid}*, Smartxpert results



Please write to contact@milvue.com for more information on Milvue integration
