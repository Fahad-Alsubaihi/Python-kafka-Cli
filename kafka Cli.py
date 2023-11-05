import subprocess
import csv
import subprocess

def run_kafka_producer(messages):
    # Command to run the Kafka Avro console producer
    command = [
        "docker", "exec", "-i", "<container_name>",
        "kafka-avro-console-producer",
        "--broker-list", "broker:9093",
        "--topic", "<topic_name>",
        "--property" ,"value.schema.id=<schema_id>",
        "--property","schema.registry.url=http://schema-registry:8081"
    ]

    # Run the command and send all messages
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for message in messages:
        process.stdin.write(message.encode('utf-8') + b'\n')

    # Close the stdin to signal the producer that there are no more messages
    process.stdin.close()

    # Wait for the process to complete
    process.wait()

    # Print the output and error messages
    output, error = process.communicate()
    print("Output:", output.decode('utf-8'))
    print("Error:", error.decode('utf-8'))

# Messages to be sent
messages = []

# Read CSV file and add Avro messages
with open('Sample5000CSVFile_556kb.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        avro_message = '{{"ID":{0},"Product":"{1}","Customer":"{2}","Quantity":{3}}}'.format(row[0], row[1], row[2], row[3])
        messages.append(avro_message)

def run_kafka_consumer():
    # Command to run the Kafka Avro console consumer
    command = [
        "docker", "exec", "-i", "<container_name>",
        "kafka-avro-console-consumer",
        "--bootstrap-server", "broker:9093",
        "--topic", "my-topic",
        "--property", "value.schema.id=58",
        "--property", "schema.registry.url=http://schema-registry:8081",
        "--max-messages", "3",
        "--from-beginning"
    ]

    # Run the command and print the output and error messages
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    print("Output:", output.decode('utf-8'))
    print("Error:", error.decode('utf-8'))
    
# Run the Kafka producer and send all messages
run_kafka_producer(messages)

# Run the Kafka consumer and read 3 messages
run_kafka_consumer()
