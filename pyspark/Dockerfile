# For more information:
#   - https://github.com/lacamposm/docker-python-envs
#   - https://hub.docker.com/r/lacamposm/docker-helpers
#   - https://github.com/lacamposm/desarrollo-analitico-oic
FROM lacamposm/docker-helpers:pyspark-conda-0.1.2

# Copy environment.yml and setup Conda environment
COPY environment.yml /tmp/environment.yml

RUN conda env update -f /tmp/environment.yml \
    && conda clean --all --yes \
    && rm /tmp/environment.yml \
    && conda init bash

# Expose port for SparkUI
EXPOSE 4040

CMD ["/bin/bash"]
