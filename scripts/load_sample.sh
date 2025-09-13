#!/usr/bin/env bash
set -euo pipefail
: "${PROJECT_ID:?set PROJECT_ID}"
bq --project_id=$PROJECT_ID load --autodetect --replace --source_format=CSV ml_trust.curated_customer_events bq/sample/curated.csv
