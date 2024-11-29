FROM ubuntu:22.10 as base 
USER root

## Setting default environment variables
ENV WEB_ROOT=/web_root
ENV APP_ROOT=${WEB_ROOT}/bcrhp
# Root project folder
ENV WHEELS=/wheels
ENV PYTHONUNBUFFERED=1
ENV NODE_MAJOR=20

RUN apt-get update && apt-get install -y make software-properties-common && apt-get install -y ca-certificates curl gnupg && mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && apt-get update

# Get the pre-built python wheels from the build environment
RUN mkdir ${WEB_ROOT}

# Install packages required to run Arches
# Note that the ubuntu/debian package for libgdal1-dev pulls in libgdal1i, which is built
# with everything enabled, and so, it has a huge amount of dependancies (everything that GDAL
# support, directly and indirectly pulling in mysql-common, odbc, jp2, perl! ... )
# a minimised build of GDAL could remove several hundred MB from the container layer.
RUN set -ex \
  && RUN_DEPS=" \
  build-essential \
  python3.11-dev \
  mime-support \
  libgdal-dev \
  python3-venv \
  postgresql-client-12 \
  python3.11 \
  python3.11-distutils \
  python3.11-venv \
  dos2unix \
  git \
  " \
  && apt-get install -y --no-install-recommends curl \
  && curl -sL https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
  && add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" \
  && apt-get update -y \
  && apt-get install -y --no-install-recommends $RUN_DEPS

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py \
  && pip install setuptools \
  && apt-get install nodejs -y \
  && npm install -g yarn \
  && rm -rf /root/.cache/pip/*

WORKDIR ${WEB_ROOT}

# Install the Arches application
# FIXME: ADD from github repository instead?

# From here, run commands from ARCHES_ROOT
COPY bcrhp/install/requirements.txt requirements.txt
RUN pip install -r requirements.txt && pip install gunicorn

COPY docker/production/entrypoint.sh ${WEB_ROOT}/entrypoint.sh
RUN chmod -R 700 ${WEB_ROOT}/entrypoint.sh &&\
  dos2unix ${WEB_ROOT}/entrypoint.sh

COPY . ${WEB_ROOT}/bcrhp

RUN mkdir /var/log/supervisor
RUN mkdir /var/log/celery

# Set default workdir
WORKDIR ${APP_ROOT}

RUN pip install .

# # Set entrypoint
ENTRYPOINT ["../entrypoint.sh"]
CMD ["run_django_server"]

# Expose port 8000
EXPOSE 8000
