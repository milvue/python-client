import os
import sys
import pydicom
from pydicom.uid import generate_uid
import milvue_sdk


API_URL = os.getenv("MILVUE_API_URL")
API_TOKEN = os.getenv("MILVUE_API_TOKEN")

# Load study dicoms + check all dicoms belong to the same study
dcm_list = [pydicom.dcmread(p) for p in sys.argv[1:]]

study_instance_uid = dcm_list[0].StudyInstanceUID
if any(dcm.StudyInstanceUID != study_instance_uid for dcm in dcm_list):
    raise Exception("All dicoms do not belong to the same study")


# if needed, renew uids
# study_instance_uid = generate_uid()
# for dcm in dcm_list:
#     dcm.StudyInstanceUID = study_instance_uid
#     dcm.SOPInstanceUID = generate_uid()

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

print("smarturgences_dicoms : ", smarturgences_dicoms)
print("----------------------------------------------------------------------------------------------------------------------------------------")
print("smarturgences_json : ", smarturgences_json)
print("----------------------------------------------------------------------------------------------------------------------------------------")
print("smartxpert_dicoms : ", smartxpert_dicoms)
print("----------------------------------------------------------------------------------------------------------------------------------------")
print("smartxpert_json : ", smartxpert_json)
