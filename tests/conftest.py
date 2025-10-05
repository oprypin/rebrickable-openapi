import os
from collections.abc import Iterator

import pytest

import rebrickable_api


@pytest.fixture(scope="session")
def api_client() -> Iterator[rebrickable_api.ApiClient]:
    configuration = rebrickable_api.Configuration(
        api_key_prefix={"HeaderAuth": "key"},
        api_key={"HeaderAuth": os.environ["REBRICKABLE_API_KEY"]},
    )
    with rebrickable_api.ApiClient(configuration) as api_client:
        yield api_client


@pytest.fixture(scope="session")
def lego_api(api_client: rebrickable_api.ApiClient) -> rebrickable_api.LegoApi:
    return rebrickable_api.LegoApi(api_client)
