ARG BASE_IMAGE=dummy

FROM ${BASE_IMAGE}

RUN pip install --no-cache-dir tensorflow~=2.19.0
