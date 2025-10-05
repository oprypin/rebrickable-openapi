## OpenAPI specification for the [Rebrickable API v3](https://rebrickable.com/api/)

This repository hosts primarily only the [openapi.yaml](openapi.yaml) file, based on which it is possible to generate comprehensive API clients as well as API documentation. There are also some supporting files around it, for running tests.

### API documentation

**[Documentation rendered in Redoc](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/oprypin/rebrickable-openapi/refs/heads/master/openapi.yaml)**

**[Documentation rendered in SwaggerUI](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/oprypin/rebrickable-openapi/refs/heads/master/openapi.yaml)**

These are generated purely from the [openapi.yaml](openapi.yaml) file.

To view the SwaggerUI page fully locally, you can run `npx open-swagger-ui --open openapi.yaml`.

### API clients

This specification can be used to generate API client libraries with fully robust type information using [`openapi-generator-cli`](https://github.com/OpenAPITools/openapi-generator-cli).

For Python, you can generate the API client using the included script [generate_python_client.sh](generate_python_client.sh). This generator output is currently not published anywhere.  
The generated API client is verified to correctly pass typechecking. This also means that you can get autocomplete for all request and response attributes in modern code editors.

This client can then be used as shown in [example.py](example.py).

The API is then also validated by Python unittests in the [tests/](tests/) directory. These also serve as further examples of the API client.  
The tests use the production Rebrickable API! They require an API token, a username and a password.

This generator should also work for many other programming languages just as well.

### Where this came from

This is based on Rebrickable's own specification, fetched on 4 Oct 2025 as follows:

```bash
curl --get 'https://converter.swagger.io/api/convert' --data-urlencode 'url=https://rebrickable.com/api/v3/swagger/?format=openapi' -H 'accept: application/yaml'
```

I then greatly expanded the documentaton, fixed a few mistakes, added full specification of the responses and examples.

This project is not affiliated with Rebrickable.
