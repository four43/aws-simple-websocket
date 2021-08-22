#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

artifacts_dir="$DIR/../artifacts"

function tf_output() {
    (
        output_name="$1"
        cd "${DIR}/../deployment" || exit 1
        terraform output --raw "$output_name"
    )
}
