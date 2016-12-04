create table DEFT_META (
META_ID NUMBER(12) PRIMARY KEY,
META_NAME VARCHAR2(128),
META_TEMPLATE NUMBER(12),
META_STATE VARCHAR2(16),
META_COMMENT VARCHAR2(128),
META_REQ_TS DATE,
META_UPD_TS DATE,
META_REQUESTOR VARCHAR2(16),
META_WORKINGGROUP VARCHAR2(32),
META_MANAGER VARCHAR2(16),
META_VO VARCHAR2(16),
META_CLOUD VARCHAR2(10),
META_SITE VARCHAR2(10),
META_PRODSOURCELABEL VARCHAR2(20),
META_ISSUE VARCHAR2(128)
)
