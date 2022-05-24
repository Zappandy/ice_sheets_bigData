# Builds a docker image for Confluent's example applications for the Kafka Streams API
ARG DOCKER_UPSTREAM_REGISTRY
ARG DOCKER_UPSTREAM_TAG=latest

FROM ${DOCKER_UPSTREAM_REGISTRY}confluentinc/cp-base-new:${DOCKER_UPSTREAM_TAG}

ARG STREAMS_VERSION
ARG PROJECT_VERSION
ARG ARTIFACT_ID
ARG GIT_COMMIT

WORKDIR /build
ENV COMPONENT="${ARTIFACT_ID}"

# We run the Kafka Streams demo application as a non-priviledged user.
ENV STREAMS_USER="streams"
ENV STREAMS_GROUP=$STREAMS_USER

# This affects how strings in Java class files are interpreted.  We want UTF-8, and this is the only locale in the
# base image that supports it
ENV LANG="C.UTF-8"

ENV STREAMS_EXAMPLES_FATJAR="ice_stream_processor-${STREAMS_VERSION}-SNAPSHOT.jar"
ENV STREAMS_APP_DIRECTORY="/usr/share/java/ice_stream_processor"
ENV STREAMS_EXAMPLES_FATJAR_DEPLOYED="$STREAMS_APP_DIRECTORY/$STREAMS_EXAMPLES_FATJAR"
ENV KAFKA_EXT_DIFF_APP_CLASS="mt.edu.um.bigdataprocessing22.group3.IceExtentDifference"

USER root

RUN groupadd $STREAMS_GROUP && useradd -r -g $STREAMS_GROUP $STREAMS_USER

RUN mkdir /etc/$COMPONENT \
  && chown $STREAMS_USER:$STREAMS_GROUP /etc/$COMPONENT

USER $STREAMS_USER

CMD ["java", "-cp", "${STREAMS_EXAMPLES_FATJAR_DEPLOYED}", "${KAFKA_EXT_DIFF_APP_CLASS}"]