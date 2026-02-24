"""Template for building a `dlt` pipeline to ingest data from a REST API."""

import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig


@dlt.source
def open_library_source():
    """Define dlt resources from REST API endpoints for Open Library."""
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://openlibrary.org/api/",
        },
        "resources": [
            {
                "name": "books",
                "endpoint": {
                    "path": "books",
                    "params": {
                        # Standard bibkeys for testing the Books API
                        "bibkeys": "ISBN:0451526538,ISBN:0385472579,ISBN:9780596513986",
                        "format": "json",
                        "jscmd": "data",
                    },
                    "data_selector": "$.*",
                },
            }
        ],
    }

    yield from rest_api_resources(config)


pipeline = dlt.pipeline(
    pipeline_name='open_library_pipeline',
    destination='duckdb',
    dataset_name='open_library_data',
    # `refresh="drop_sources"` ensures the data and the state is cleaned
    # on each `pipeline.run()`; remove the argument once you have a
    # working pipeline.
    refresh="drop_sources",
)


if __name__ == "__main__":
    load_info = pipeline.run(open_library_source())
    print(load_info)

