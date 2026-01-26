variable "credentials" {
  description = "Path to the GCP credentials JSON file"
  default     = "/home/codespace/.gcp/sa-key.json"
}

variable "project_id" {
  description = "The GCP project ID"
  default     = "terraform-setup-485500"
}

variable "location" {
  description = "The GCP region"
  default     = "US"
}

variable "region" {
  description = "The GCP location for the storage bucket"
  default     = "us-central1"
}

variable "bucket_name" {
  description = "The name of the GCS bucket"
  default     = "terraform-setup-485500-data-bucket"
}

variable "gcs_storage_class" {
  description = "The GCS storage class"
  default     = "STANDARD"
}

variable "bq_dataset_id" {
  description = "The BigQuery dataset ID"
  default     = "zoomcamp_dataset"
}
