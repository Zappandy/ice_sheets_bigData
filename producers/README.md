The producers can be controlled by sending a JSON message to the "control" topic.
We can adjust speed (lower is faster, higher is slower, 0 is fastest) and pause and resume data streaming

For starting a kafka console control producer:
```
bash kafka-console-producer.sh --bootstrap-server localhost:9092 --topic control
```

The control message specifies which topic and which parameter to control
```
{"topic":"icesheets","pause":true}

{"topic":"icesheets","pause":false}

{"topic":"icesheets","speed":100}
```
faster
```
{"topic":"icesheets","speed":100,"pause":false}
```
slower
```
{"topic":"icesheets","speed":1000,"pause":false} # slower
```
