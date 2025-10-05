#!/bin/bash

set -e -u -x
cd "$(dirname "$0")"

openapi-generator-cli generate \
    --remove-operation-id-prefix \
    --api-name-suffix='' \
    --skip-operation-example \
    --strict-spec=true \
    --package-name=rebrickable_api \
    --global-property={generateSourceCodeOnly=true,apiDocs=false,modelDocs=false,apiTests=false,modelTests=false} \
    --generator-name python \
    --additional-properties=hideGenerationTimestamp=true \
    -i openapi.yaml
