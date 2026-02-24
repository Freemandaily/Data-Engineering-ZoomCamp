"""NYC taxi data ingestion pipeline using dlt rest_api source."""

import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig


@dlt.source
def homework_taxi_pipeline_rest_api_source():
    """Define dlt resources from NYC Taxi REST API."""
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/",
        },
        "resources": [
            {
                "name": "taxi_records",
                "endpoint": {
                    "path": "data_engineering_zoomcamp_api",
                    "paginator": {
                        "type": "page_number",
                        "page_param": "page",
                        "base_page": 1,
                        "total_path": None,
                        "stop_after_empty_page": True,
                    },
                },
            },
        ],
    }

    yield from rest_api_resources(config)


pipeline = dlt.pipeline(
    pipeline_name='taxi_pipeline',
    destination='duckdb',
    dataset_name='taxi_raw_data',
    progress="log",
    refresh="drop_sources",
)


if __name__ == "__main__":
    load_info = pipeline.run(homework_taxi_pipeline_rest_api_source())
    print(load_info)  # noqa: T201
