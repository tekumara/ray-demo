FROM rayproject/ray:2.2.0-py39-cpu

RUN pip install --no-cache-dir tensorflow~=2.11.0
