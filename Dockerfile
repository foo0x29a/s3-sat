FROM python:3.8.5-slim as base

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

FROM base as build

COPY setup.py /
COPY s3_sat /s3_sat

RUN python3 setup.py sdist bdist_wheel

FROM base

COPY --from=build /dist/s3-sat-0.0.1.tar.gz /
RUN python3 -m pip install s3-sat-0.0.1.tar.gz

ENTRYPOINT ["python3", "-m", "s3_sat"]
