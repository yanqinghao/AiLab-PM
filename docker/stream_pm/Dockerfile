ARG PYTHON_VERSION=3.7

ARG NAME_SPACE

FROM registry-vpc.cn-shanghai.aliyuncs.com/${NAME_SPACE}/stream_base:${PYTHON_VERSION} as builder

ENV PYPI_MIRROR "https://mirrors.aliyun.com/pypi/simple"

RUN pip config set global.index-url ${PYPI_MIRROR}

RUN pip install --upgrade pip

RUN pip install --no-cache-dir pyarmor

WORKDIR /build

COPY . /build

RUN bash tools/compress.sh

FROM registry-vpc.cn-shanghai.aliyuncs.com/${NAME_SPACE}/stream_base:${PYTHON_VERSION}

WORKDIR /workspace

ENV PYPI_MIRROR "https://mirrors.aliyun.com/pypi/simple"

RUN pip config set global.index-url ${PYPI_MIRROR}

RUN pip install --upgrade pip

RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt-get install graphviz -y

COPY --from=builder /build /workspace

RUN pip install -r requirements.txt

ENTRYPOINT [ "/sbin/my_init", "--" ]

CMD [ "bash" ]
