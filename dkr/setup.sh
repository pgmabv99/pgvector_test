#!/bin/bash
set -x
# Get the root directory of the Git repository
git_root=$(git rev-parse --show-toplevel)

image_dep=dep:latest
cnt_dep=cnt_dep
image_pgv=pgv:latest
cnt_pgv=cnt_pgv
# cnt_user=root
cnt_user=postgres
