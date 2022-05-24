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

ADD ./target/ice_stream_processors-1.0-SNAPSHOT-jar-with-dependencies.jar ./

ENV FATJAR="ice_stream_processors-1.0-SNAPSHOT-jar-with-dependencies.jar"
ENV KAFKA_EXT_DIFF_APP_CLASS="mt.edu.um.bigdataprocessing22.group3.IceExtentDifference"

USER root

RUN groupadd $STREAMS_GROUP && useradd -r -g $STREAMS_GROUP $STREAMS_USER

RUN mkdir /etc/$COMPONENT \
  && chown $STREAMS_USER:$STREAMS_GROUP /etc/$COMPONENT

USER $STREAMS_USER
#ENV ENV_VARIABLE_TEST="myvariable_dockerfile"
# CMD ["sh", "-c", "echo ${ENV_VARIABLE_TEST}"]
CMD ["java", "-cp", "ice_stream_processors-1.0-SNAPSHOT-jar-with-dependencies.jar", "mt.edu.um.bigdataprocessing22.group3.IceExtentDifference"]
# CMD ["sh", "-c", "echo", "$STREAMS_EXAMPLES_FATJAR_DEPLOYED", "$KAFKA_EXT_DIFF_APP_CLASS"]