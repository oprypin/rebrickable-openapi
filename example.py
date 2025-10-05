import os

import rebrickable_api

configuration = rebrickable_api.Configuration(
    api_key_prefix={"HeaderAuth": "key"},
    api_key={"HeaderAuth": os.environ["REBRICKABLE_API_KEY"]},
)
api_client = rebrickable_api.ApiClient(configuration)

lego_api = rebrickable_api.LegoApi(api_client)
users_api = rebrickable_api.UsersApi(api_client)

print(lego_api.get_color(id=72).name)  # => Dark Bluish Gray

user_token = users_api.create_user_token(
    os.environ["REBRICKABLE_USERNAME"], os.environ["REBRICKABLE_PASSWORD"]
).user_token

for a_set in users_api.list_sets(user_token).results:
    print(a_set.set.name)  # => Super Robot
