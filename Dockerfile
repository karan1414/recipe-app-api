# # name of the image we will be pulling from dockerhub that is the base of our project
# FROM python:3.9-alpine3.13
# LABEL maintainer="karan1395"

# ENV PYTHONUNBUFFERED 1

# COPY ./requirements.txt /tmp/requirements.txt
# COPY ./requirements.dev.txt /tmp/requirements.dev.txt 
# COPY ./app /app
# WORKDIR /app 
# EXPOSE 8000

# ARG DEV=false

# # Below we are defining a run command using all command at once
# # seperated by && \
# # Running different run commands create different layers of images in our system.

# # -m venv /py && \ ---creating virtual env
# # /py/bin/pip install --upgrade pip && \ ---> upgrade pip inside virtual env
# # /py/bin/pip install -r /tmp/requirements.txt && \  ----> install requirements fro requirement file
# # rm -rf /tmp && \ ---> remove /tmp directory to remove all temporary files
# #     adduser \    ---> to avoid using root user we add a user
#         # --disabled-password \
#         # --no-create-home \ 
#         # django-user
# RUN python -m venv /py && \ 
#     /py/bin/pip install --upgrade pip && \
#     /py/bin/pip install -r /tmp/requirements.txt && \
#     if [ $DEV = "true" ]; \
#         then /py/bin/pip install -r /tmp/requirements.dev.txt; \
#     fi &&\
#     rm -rf /tmp && \
#     adduser \
#         --disabled-password \
#         --no-create-home \ 
#         django-user
# # django-user can be any name that we want to give
# # env variable inside the image
# # 
# ENV PATH="/py/bin:$PATH"

# # should be the last line
# # django user name we are switching to
# USER django-user

FROM python:3.9-alpine3.13
LABEL maintainer="karan1395"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# Below we are defining a run command using all command at once
# seperated by && \
# Running different run commands create different layers of images in our system.

# -m venv /py && \ ---creating virtual env
# /py/bin/pip install --upgrade pip && \ ---> upgrade pip inside virtual env
# /py/bin/pip install -r /tmp/requirements.txt && \  ----> install requirements fro requirement file
# rm -rf /tmp && \ ---> remove /tmp directory to remove all temporary files
#     adduser \    ---> to avoid using root user we add a user
        # --disabled-password \
        # --no-create-home \ 
        # django-user
ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
# django-user can be any name that we want to give
# env variable inside the image

ENV PATH="/py/bin:$PATH"

# should be the last line
# django user name we are switching to
USER django-user