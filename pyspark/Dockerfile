FROM continuumio/miniconda3:24.11.1-0

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    wget \
    sudo \
    bash-completion \
    locales \
    build-essential \
    make \
    postgresql-client \
    libnss3 \
    git \
    openjdk-17-jre-headless \
    && git config --system core.sshCommand "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" \
    && git config --system --add safe.directory "*" \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /data/_tmp && \
    chmod -R 777 /data/_tmp && \
    wget -q https://archive.apache.org/dist/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz && \
    tar -xzf spark-3.5.5-bin-hadoop3.tgz && \
    mv spark-3.5.5-bin-hadoop3 /opt/spark && \
    rm spark-3.5.5-bin-hadoop3.tgz && \
    rm -rf /tmp/* /root/.cache /root/.wget-hsts

COPY environment.yml /tmp/environment.yml
RUN conda env update -f /tmp/environment.yml \
    && conda clean --all --yes \
    && rm /tmp/environment.yml \
    && conda init bash

ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

EXPOSE 4040 8888

CMD ["/bin/bash"]
