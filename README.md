# A Python Client for Milvue API v3

This package allows to POST studies and GET results to/from Milvue API (https://milvue.com)

It implements STOW and WADO protocols from the DICOMweb Standard, https://www.dicomstandard.org/using/dicomweb

In addition, the following Pydantic Schemas (generated with https://github.com/deepmap/oapi-codegen) describe JSON responses for non-DICOMweb routes:

- `GetStatusResponseV3`: schema for *v3/studies/{study_instance_uid}/status*, the current prediction status
- `GetSmarturgencesResponseV3`: schema for *v3/smarturgences/{study_instance_uid}*, Smarturgences results
- `GetSmartxpertResponseV3`: schema for *v3/smartxpert/{study_instance_uid}*, Smartxpert results

Please write to contact@milvue.com for more information on Milvue integration
