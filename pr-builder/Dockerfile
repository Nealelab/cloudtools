FROM alpine:3.8

RUN apk --no-cache add python3 bash git openssh curl

RUN adduser -S -s /bin/bash cloudtools
USER cloudtools
WORKDIR /home/cloudtools

# this seems easier than getting the keys right for apt
#
# source: https://cloud.google.com/storage/docs/gsutil_install#linux
RUN /bin/sh -c 'curl https://sdk.cloud.google.com | bash'
ENV PATH $PATH:/home/cloudtools/google-cloud-sdk/bin

VOLUME /secrets
WORKDIR /
