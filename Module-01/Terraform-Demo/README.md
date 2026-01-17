# Terraform Setup and Usage Guide

This guide documents the setup and usage of Terraform for Google Cloud Platform (GCP).

## Prerequisites

1.  **GCP Account:** Ensure you have an active Google Cloud Platform account.
2.  **Service Account Key:** Create a service account in GCP and download the JSON key file.
3.  **Terraform:** Install Terraform and the Terraform extension for VS Code.

## 1. Project Setup

Open your terminal and set up the project directory structure:

```bash
mkdir Terraform-Demo
cd Terraform-Demo
mkdir keys
cd keys
# Create/Paste your credentials file
nano my-creds.json
```

## 2. Provider Configuration

1.  Visit the [Terraform Google Provider Registry](https://registry.terraform.io/providers/hashicorp/google/latest/docs) to check for the latest version.
2.  Create a file named `main.tf` in the root directory (`Terraform-Demo`).
3.  Add the following configuration:

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.16.0" # Check for the latest version
    }
  }
}

provider "google" {
  project = "my-project-id"
  region  = "us-central1"
}
```

4.  Replace `"my-project-id"` with your actual GCP Project ID.
5.  **Authentication:** Export your credentials to the environment variables (recommended):

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/Terraform-Demo/keys/my-creds.json"
```

6.  Initialize Terraform:

```bash
terraform init
```

## 3. Creating Resources

### GCP Storage Bucket

Documentation: Google Storage Bucket

Add the following resource to `main.tf`. Ensure the bucket name is globally unique.

```hcl
resource "google_storage_bucket" "demo-bucket" {
  name                        = "terraform-484123-terraform-bucket" # Change to a unique name
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}
```

### GCP BigQuery Dataset

Documentation: [Google BigQuery Dataset](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset)

Add the following resource to `main.tf`:

```hcl
resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = "example_dataset"
}
```

**Tip:** Use `terraform fmt` to format your code automatically.

### Execution

Run the following commands to preview and apply changes:

```bash
terraform plan
terraform apply
```

To remove resources:

```bash
terraform destroy
```

## 4. Using Terraform Variables

Variables allow you to parameterize your configuration.

1.  Create a file named `variables.tf` in the root directory.
2.  Add the following content:

```hcl
variable "credentials" {
  description = "Path to the service account key file"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "GCP Project ID"
  default     = "terraform-484415"
}

variable "region" {
  description = "GCP Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "Storage Bucket Name"
  default     = "terraform-484415-terraform-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}
```

3.  Update `main.tf` to use these variables:

```hcl
terraform {
    required_providers {
        google = {
        source  = "hashicorp/google"
        version = "5.16.0"
        }
    }
}

provider "google" {
    credentials = file(var.credentials)
    project     = var.project
    region      = var.region
}

resource "google_storage_bucket" "demo-bucket" {
    name                        = var.gcs_bucket_name
    location                    = var.location
    force_destroy               = true
    uniform_bucket_level_access = true

    lifecycle_rule {
        condition {
        age = 1
        }
        action {
        type = "AbortIncompleteMultipartUpload"
        }
    }
}

resource "google_bigquery_dataset" "demo_dataset" {
    dataset_id = var.bq_dataset_name
}
```

**Note:** If using `credentials` in the provider block, you can unset the environment variable:
```bash
unset GOOGLE_APPLICATION_CREDENTIALS
```

## Security Best Practices

1.  **Gitignore:** Always include a `.gitignore` file to prevent committing sensitive data.
2.  **Reference:** Terraform .gitignore template
3.  **Important:** Never push your service account keys (`*.json`) to a public repository.
