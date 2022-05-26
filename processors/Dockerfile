# Builds a docker image for Confluent's example applications for the Kafka Streams API
ARG DOCKER_UPSTREAM_TAG=latest

FROM confluentinc/cp-base-new:${DOCKER_UPSTREAM_TAG}

ARG VERSION="1.0"
ARG ARTIFACT_ID="IceExtentDifference"

WORKDIR /build
ENV COMPONENT="${ARTIFACT_ID}"

# We run the Kafka Streams demo application as a non-priviledged user.
ENV STREAMS_USER="streams"
ENV STREAMS_GROUP=$STREAMS_USER

# This affects how strings in Java class files are interpreted.  We want UTF-8, and this is the only locale in the
# base image that supports it
ENV LANG="C.UTF-8"
ENV FATJAR="ice_stream_processors-1.0-SNAPSHOT-jar-with-dependencies.jar"

ADD ./target/$FATJAR ./

USER root

RUN groupadd $STREAMS_GROUP && useradd -r -g $STREAMS_GROUP $STREAMS_USER

RUN mkdir /etc/$COMPONENT \
  && chown $STREAMS_USER:$STREAMS_GROUP /etc/$COMPONENT

USER $STREAMS_USER

# CMD ["java", "-cp", "ice_stream_processors-1.0-SNAPSHOT-jar-with-dependencies.jar", "mt.edu.um.bigdataprocessing22.group3.IceExtentDifference"]
CMD ["sh", "-c", "java -cp ${FATJAR} ${APP_CLASS}"]