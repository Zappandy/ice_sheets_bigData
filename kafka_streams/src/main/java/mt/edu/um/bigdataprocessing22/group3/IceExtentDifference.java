package mt.edu.um.bigdataprocessing22.group3;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Produced;

import java.io.IOException;
import java.util.Properties;

public class IceExtentDifference {
    public static void main(String[] args) throws IOException {
        System.out.println("starting IceExtentDifference processor...");
        final String KAFKA_BROKER_URL = System.getenv("KAFKA_BROKER_URL");
        final String inputTopic = System.getenv("LISTEN_TO_TOPICS");
        final int LISTENER_TIMEOUT = Integer.parseInt(System.getenv("LISTENER_TIMEOUT"));
        final String outputTopic = System.getenv("TOPIC_NAME");

        Properties streamsProps = new Properties();
        streamsProps.put(StreamsConfig.APPLICATION_ID_CONFIG, "ice_extent_difference");
        streamsProps.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, KAFKA_BROKER_URL);

        StreamsBuilder builder = new StreamsBuilder();

        KStream<String, String> firstStream = builder.stream(inputTopic, Consumed.with(Serdes.String(), Serdes.String()));

        firstStream.peek((key, value) -> System.out.println("Incoming record - key " + key +" value " + value))
                .to(outputTopic, Produced.with(Serdes.String(), Serdes.String()));

        KafkaStreams kafkaStreams = new KafkaStreams(builder.build(), streamsProps);
        // TopicLoader.runProducer();
        kafkaStreams.start();
    }

}
