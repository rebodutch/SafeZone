ARG BASE_IMAGE_TAG=latest
FROM safezone-cli-command:${BASE_IMAGE_TAG}

ENV PYTHONUNBUFFERED=1

COPY toolkit/cli/ops/smoke_test.py /app/smoke_test.py
COPY toolkit/cli/ops/test_cases /app/test_cases
COPY toolkit/cli/ops/routines /app/routines

# No ENTRYPOINT: every consumer (compose, the safezone-ops chart) declares its
# command explicitly; WORKDIR /app keeps smoke_test.py's relative paths valid.
WORKDIR /app
