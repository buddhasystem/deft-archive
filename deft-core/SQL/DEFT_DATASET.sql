create table DEFT_DATASET (
DATASET_ID NUMBER(12) PRIMARY KEY,
DATASET_NAME VARCHAR2(256),
DATASET_META NUMBER(12),
DATASET_STATE VARCHAR2(16),
DATASET_SOURCE NUMBER(12),
DATASET_TARGET NUMBER(12),
DATASET_COMMENT VARCHAR2(256),
DATASET_FLAVOR VARCHAR2(16),
DATASET_FORMAT VARCHAR2(16),
DATASET_TOKEN VARCHAR2(60),
DATASET_OFFSET NUMBER(12)

)
