#!/usr/bin/env bash
set -euo pipefail
: "${PROJECT_ID:?set PROJECT_ID}"
gcloud services enable dlp.googleapis.com datacatalog.googleapis.com bigquery.googleapis.com
