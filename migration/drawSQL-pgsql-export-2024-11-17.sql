CREATE TABLE "Datasets"(
    "dataset_id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "type" VARCHAR(255) NOT NULL,
    "created_at" DATE NOT NULL
);
ALTER TABLE
    "Datasets" ADD PRIMARY KEY("dataset_id");
CREATE TABLE "Error_Metadata"(
    "metadata_id" BIGINT NOT NULL,
    "error_id" BIGINT NOT NULL,
    "key" VARCHAR(255) NOT NULL,
    "value" TEXT NOT NULL
);
ALTER TABLE
    "Error_Metadata" ADD PRIMARY KEY("metadata_id");
CREATE TABLE "Training_Metrics"(
    "metric_id" BIGINT NOT NULL,
    "session_id" BIGINT NOT NULL,
    "metric_name" VARCHAR(255) NOT NULL,
    "metric_value" FLOAT(53) NOT NULL,
    "epoch" BIGINT NOT NULL
);
ALTER TABLE
    "Training_Metrics" ADD PRIMARY KEY("metric_id");
CREATE TABLE "Version_Status"(
    "status_id" BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "status_date" DATE NOT NULL
);
ALTER TABLE
    "Version_Status" ADD PRIMARY KEY("status_id");
CREATE TABLE "Dataset_Metadata"(
    "metadata_id" BIGINT NOT NULL,
    "dataset_id" BIGINT NOT NULL,
    "key" VARCHAR(255) NOT NULL,
    "value" TEXT NOT NULL
);
ALTER TABLE
    "Dataset_Metadata" ADD PRIMARY KEY("metadata_id");
CREATE TABLE "Session_Status"(
    "status_id" BIGINT NOT NULL,
    "session_id" BIGINT NOT NULL,
    "status" VARCHAR(255) NOT NULL,
    "status_date" DATE NOT NULL
);
ALTER TABLE
    "Session_Status" ADD PRIMARY KEY("status_id");
CREATE TABLE "Model_Versions"(
    "version_id" BIGINT NOT NULL,
    "model_id" BIGINT NOT NULL,
    "version_number" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "Model_Versions" ADD PRIMARY KEY("version_id");
CREATE TABLE "Users"(
    "user_id" BIGINT NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "role" VARCHAR(255) NOT NULL,
    "created_at" DATE NOT NULL
);
ALTER TABLE
    "Users" ADD PRIMARY KEY("user_id");
CREATE TABLE "Training_Sessions"(
    "sessions_id" BIGINT NOT NULL,
    "model_id" BIGINT NOT NULL,
    "dataset_id" BIGINT NOT NULL,
    "start_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "end_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "Training_Sessions" ADD PRIMARY KEY("sessions_id");
CREATE TABLE "Error_Logs"(
    "error_id" BIGINT NOT NULL,
    "timestamp" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "error_level" VARCHAR(255) NOT NULL,
    "message" TEXT NOT NULL,
    "service_name" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "Error_Logs" ADD PRIMARY KEY("error_id");
CREATE TABLE "Model_Parameters"(
    "parameter_id" BIGINT NOT NULL,
    "version_id" BIGINT NOT NULL,
    "parameter_name" VARCHAR(255) NOT NULL,
    "parameter_value" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "Model_Parameters" ADD PRIMARY KEY("parameter_id");
CREATE TABLE "User_Permissions"(
    "permission_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "permission_type" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "User_Permissions" ADD PRIMARY KEY("permission_id");
CREATE TABLE "Models"(
    "model_id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "type" VARCHAR(255) NOT NULL,
    "creation_date" DATE NOT NULL,
    "last_update" DATE NOT NULL
);
ALTER TABLE
    "Models" ADD PRIMARY KEY("model_id");
ALTER TABLE
    "Version_Status" ADD CONSTRAINT "version_status_version_id_foreign" FOREIGN KEY("version_id") REFERENCES "Model_Versions"("version_id");
ALTER TABLE
    "Model_Versions" ADD CONSTRAINT "model_versions_model_id_foreign" FOREIGN KEY("model_id") REFERENCES "Models"("model_id");
ALTER TABLE
    "Error_Metadata" ADD CONSTRAINT "error_metadata_error_id_foreign" FOREIGN KEY("error_id") REFERENCES "Error_Logs"("error_id");
ALTER TABLE
    "User_Permissions" ADD CONSTRAINT "user_permissions_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "Users"("user_id");
ALTER TABLE
    "Session_Status" ADD CONSTRAINT "session_status_session_id_foreign" FOREIGN KEY("session_id") REFERENCES "Training_Sessions"("sessions_id");
ALTER TABLE
    "Training_Sessions" ADD CONSTRAINT "training_sessions_dataset_id_foreign" FOREIGN KEY("dataset_id") REFERENCES "Datasets"("dataset_id");
ALTER TABLE
    "Training_Sessions" ADD CONSTRAINT "training_sessions_model_id_foreign" FOREIGN KEY("model_id") REFERENCES "Models"("model_id");
ALTER TABLE
    "Training_Metrics" ADD CONSTRAINT "training_metrics_session_id_foreign" FOREIGN KEY("session_id") REFERENCES "Training_Sessions"("sessions_id");
ALTER TABLE
    "Model_Parameters" ADD CONSTRAINT "model_parameters_version_id_foreign" FOREIGN KEY("version_id") REFERENCES "Model_Versions"("version_id");
ALTER TABLE
    "Dataset_Metadata" ADD CONSTRAINT "dataset_metadata_dataset_id_foreign" FOREIGN KEY("dataset_id") REFERENCES "Datasets"("dataset_id");