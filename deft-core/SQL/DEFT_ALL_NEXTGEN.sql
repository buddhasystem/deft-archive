BEGIN;
CREATE TABLE "DEFT_META" (
    "META_ID" decimal NOT NULL PRIMARY KEY,
    "META_STATE" varchar(16) NOT NULL,
    "META_COMMENT" varchar(128) NOT NULL,
    "META_REQUESTOR" varchar(128) NOT NULL,
    "META_MANAGER" varchar(128) NOT NULL,
    "META_VO" varchar(16) NOT NULL,
    "meta_req_ts" datetime NOT NULL,
    "meta_upd_ts" datetime NOT NULL
)
;
CREATE TABLE "DEFT_TASK" (
    "TASK_ID" decimal NOT NULL PRIMARY KEY,
    "task_meta_id" decimal NOT NULL UNIQUE REFERENCES "DEFT_META" ("META_ID"),
    "TASK_COMMENT" varchar(128) NOT NULL,
    "task_dataset_id" decimal NOT NULL,
    "task_destination_id" decimal NOT NULL,
    "TASK_DISKCOUNT" smallint unsigned NOT NULL,
    "TASK_EVENTS_PER_JOB" integer unsigned NOT NULL,
    "TASK_FORMATS" varchar(80) NOT NULL,
    "task_group_id" decimal NOT NULL,
    "TASK_LUMIBLOCK" bool NOT NULL,
    "TASK_NUM_EVENTS" smallint unsigned NOT NULL,
    "task_owner_id" decimal NOT NULL,
    "TASK_PARAM" varchar(4000) NOT NULL,
    "TASK_PRIORITY" smallint unsigned NOT NULL,
    "task_project_id" decimal NOT NULL,
    "TASK_PROJECT_MODE" varchar(300) NOT NULL,
    "TASK_RAM" smallint unsigned NOT NULL,
    "TASK_REPROCESSING" bool NOT NULL,
    "TASK_STATE" varchar(16) NOT NULL,
    "TASK_TAG" varchar(20) NOT NULL,
    "TASK_TOTAL_GENEVENTS" integer NOT NULL,
    "TASK_TRANSPATH" varchar(128) NOT NULL,
    "TASK_VO" varchar(16) NOT NULL,
    "slug" varchar(50) NOT NULL UNIQUE
)
;
CREATE TABLE "DEFT_USERS" (
    "TASK_ID" decimal NOT NULL PRIMARY KEY,
    "USER_NAME" varchar(128) NOT NULL,
    "USER_DN" varchar(100) NOT NULL,
    "USER_EMAIL" varchar(274) NOT NULL,
    "user_group_id" decimal NOT NULL,
    "user_project_id" decimal NOT NULL,
    "user_vo_id" decimal NOT NULL,
    "USER_TAG" varchar(20) NOT NULL,
    "user_location_id" decimal NOT NULL,
    "slug" varchar(50) NOT NULL UNIQUE
)
;
CREATE TABLE "DEFT_GROUPS" (
    "GROUP_ID" decimal NOT NULL PRIMARY KEY,
    "GROUP_NAME" varchar(128) NOT NULL,
    "group_vo_id" decimal NOT NULL,
    "GROUP_TAG" varchar(20) NOT NULL,
    "GROUP_DESCRIPTION" varchar(100) NOT NULL,
    "GROUP_CONTACTEMAIL" varchar(274) NOT NULL,
    "slug" varchar(50) NOT NULL UNIQUE
)
;
CREATE TABLE "DEFT_PROJECT" (
    "PROJ_ID" decimal NOT NULL PRIMARY KEY,
    "PROJ_NAME" varchar(128) NOT NULL,
    "proj_vo_id" decimal NOT NULL,
    "PROJ_TAG" varchar(20) NOT NULL,
    "PROJ_DESCRIPTION" varchar(200) NOT NULL,
    "PROJ_CONTACTEMAIL" varchar(274) NOT NULL,
    "slug" varchar(50) NOT NULL UNIQUE
)
;
CREATE TABLE "DEFT_VO" (
    "VO_ID" decimal NOT NULL PRIMARY KEY,
    "VO_NAME" varchar(16) NOT NULL,
    "slug" varchar(50) NOT NULL UNIQUE
)
;
CREATE TABLE "DEFT_LOCATION" (
    "LOC_ID" decimal NOT NULL PRIMARY KEY,
    "LOC_NAME" varchar(64) NOT NULL,
    "LOC_COUNTRY" varchar(64) NOT NULL,
    "LOC_REGION" varchar(64) NOT NULL,
    "loc_vo_id" decimal NOT NULL REFERENCES "DEFT_VO" ("VO_ID"),
    "slug" varchar(50) NOT NULL UNIQUE
)
;
CREATE TABLE "DEFT_SE" (
    "SE_ID" decimal NOT NULL PRIMARY KEY,
    "SE_NAME" varchar(90) NOT NULL,
    "se_location_id" decimal NOT NULL REFERENCES "DEFT_LOCATION" ("LOC_ID"),
    "slug" varchar(50) NOT NULL UNIQUE
)
;
CREATE TABLE "DEFT_DATASET" (
    "DATASET_ID" decimal NOT NULL PRIMARY KEY,
    "DATASET_NAME" varchar(128) NOT NULL,
    "DATASET_SOURCE" decimal NOT NULL,
    "DATASET_TARGET" decimal NOT NULL,
    "DATASET_META" decimal NOT NULL,
    "DATASET_STATE" varchar(16) NOT NULL,
    "DATASET_FLAVOR" varchar(16) NOT NULL,
    "DATASET_FORMAT" varchar(16) NOT NULL,
    "DATASET_COMMENT" varchar(128) NOT NULL,
    "slug" varchar(50) NOT NULL UNIQUE
)
;
CREATE TABLE "PRODSYS_COMM" (
    "COMM_TASK" decimal NOT NULL PRIMARY KEY,
    "COMM_META" decimal NOT NULL,
    "COMM_OWNER" varchar(16) NOT NULL,
    "COMM_CMD" varchar(256) NOT NULL,
    "COMM_TS" decimal NOT NULL,
    "COMM_COMMENT" varchar(128) NOT NULL,
    "slug" varchar(50) NOT NULL UNIQUE
)
;
CREATE INDEX "DEFT_TASK_f54ce2f7" ON "DEFT_TASK" ("task_dataset_id");
CREATE INDEX "DEFT_TASK_0930ded8" ON "DEFT_TASK" ("task_destination_id");
CREATE INDEX "DEFT_TASK_841042a0" ON "DEFT_TASK" ("task_group_id");
CREATE INDEX "DEFT_TASK_3b61c88f" ON "DEFT_TASK" ("task_owner_id");
CREATE INDEX "DEFT_TASK_49e291f4" ON "DEFT_TASK" ("task_project_id");
CREATE INDEX "DEFT_USERS_1a56174b" ON "DEFT_USERS" ("user_group_id");
CREATE INDEX "DEFT_USERS_92c62c6f" ON "DEFT_USERS" ("user_project_id");
CREATE INDEX "DEFT_USERS_bb9c44d7" ON "DEFT_USERS" ("user_vo_id");
CREATE INDEX "DEFT_USERS_705cfe0c" ON "DEFT_USERS" ("user_location_id");
CREATE INDEX "DEFT_GROUPS_d806aeae" ON "DEFT_GROUPS" ("group_vo_id");
CREATE INDEX "DEFT_PROJECT_45e0b1e1" ON "DEFT_PROJECT" ("proj_vo_id");
CREATE INDEX "DEFT_LOCATION_ad48c5f9" ON "DEFT_LOCATION" ("loc_vo_id");
CREATE INDEX "DEFT_SE_0aac1c23" ON "DEFT_SE" ("se_location_id");

COMMIT;

