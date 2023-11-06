import subprocess
import sys
import logging


logging.basicConfig(filename='consumer_group_lag.log', level=logging.INFO)

# Add a StreamHandler to output log messages to the console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

def check_consumer_group_lag(acceptable_lag):
    """
    This function checks the lag of each consumer group and returns a list of groups with lag greater than the acceptable lag.

    Parameters:
    acceptable_lag (int): The maximum acceptable lag for a consumer group.

    Returns:
    list: A list of consumer groups with lag greater than the acceptable lag.
    """
    potential_error_groups = []

    # Get the list of consumer groups
    command = "docker exec -i kafka-cli kafka-consumer-groups --bootstrap-server broker:9093 --list"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    # to print all the consumers groups
    print("Output:", output.decode('utf-8'))
    # print("Error:", error.decode('utf-8'))
   
    consumer_groups = output.decode().splitlines()
    # print (consumer_groups)
# describe every consumer group and check for lag

    for consumer_group in consumer_groups:

        if consumer_group:
        
            command = f"docker exec -i kafka-cli kafka-consumer-groups --bootstrap-server broker:9093 --describe --group {consumer_group}"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output, error = process.communicate()
            # print("Output:", output.decode('utf-8'))

            output_lines = output.decode().splitlines()[2:]
            # print(output_lines)

            # check if lag is more than acceptable_lag and add to list potential_error_groups
            

            for line in output_lines:

                fields = line.split()

            # some time lag is not a number, so we need to check if it is a number or not
                try:
                    # if the lag is more than acceptable_lag
                    if int(fields[5]) > acceptable_lag:
                        # add the group to list potential_error_groups
                        potential_error_groups.append(line)
                        logging.info(f"Consumer group {consumer_group} has a lag of {fields[5]} which is greater than the acceptable lag of {acceptable_lag}")
                
                except ValueError:
                    # Handle the case where value is not an integer
                    print(f"skip '{fields[5]}' is not an integer")
            
    # return the list of potential_error_groups
    return potential_error_groups


if __name__ == "__main__":
    # Run the check_consumer_group_lag function
    errors = check_consumer_group_lag(5000)

    # print the errors
    for error in errors:
        print(error)
                    

