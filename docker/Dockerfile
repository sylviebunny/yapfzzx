FROM python

ARG YAPF_VERSION

COPY script/entrypoint.sh entrypoint.sh

RUN pip install yapf==0.20.2

ENTRYPOINT ["./entrypoint.sh"]
