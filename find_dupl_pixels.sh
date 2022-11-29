#!/usr/bin/env bash

# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT

set -e
set -o pipefail
set -u

argc="$#"

if [ $argc -lt 1 ]; then
  2>&1 echo "Usage: $0 cooler [cpus] [memory]"
  2>&1 echo "Example: $0 4DNFI9GMP2J8.mcool::/resolutions/2000 8 16G"
  exit 1
fi

if [ $argc -ge 2 ]; then
  cpus="$2"
else
  cpus=$(nproc)
fi

if [ $argc -ge 3 ]; then
  memory="$3"
else
  memory='16G'
fi


# Print duplicate BEDPE records (ignoring the value field)
cooler dump --join --no-balance "$1"   |
  sort --parallel="$cpus" -S "$memory" |
  rev | uniq --skip-fields=1 -D | rev
