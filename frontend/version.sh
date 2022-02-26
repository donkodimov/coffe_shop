#!/usr/bin/env bash
## Use git commit hash as version and image tag.
myfunc() {
  GIT_HASH=$(git rev-parse HEAD)
  local ver=${GIT_HASH::7}
  echo $ver
}

myfunc