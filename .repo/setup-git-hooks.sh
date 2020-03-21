#!/bin/bash
set -e

THIS_FOLDER="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
GIT_FOLDER=$(git rev-parse --show-toplevel)/.git

cp -a "$THIS_FOLDER/hooks/." "$GIT_FOLDER/hooks/"
