#!/bin/bash

version_regex="[0-9a-zA-Z\.]+"

if [[ -n $INPUT_PACKAGE_MANAGER ]]
then
    if [[ "$INPUT_PACKAGE_MANAGER" == "pipenv" ]]
    then
        cat Pipfile.lock | jq --raw-output '."'"$INPUT_GROUP"'"."'"$INPUT_PACKAGE"'".version' | grep -Po $version_regex
    elif [ "$INPUT_PACKAGE_MANAGER}" == "poetry" ]
    then
        poetry show --with="$INPUT_GROUP" -- "$INPUT_PACKAGE" | grep "version" | grep -o ": .*" | grep -Po $version_regex
    elif [[ "$INPUT_PACKAGE_MANAGER}" == "pip" ]]
    then
        cat $INPUT_REQUIREMENTS_FILE | grep "$INPUT_PACKAGE" | grep -Po "[=><~]+.*" | grep -Po $version_regex
    else
        echo "Invalid package manager: $INPUT_PACKAGE_MANAGER"
        exit 1
    fi
else
    echo "INPUT_PACKAGE_MANAGER not set"
    exit 1
fi
