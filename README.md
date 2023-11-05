# Python-kafka-Cli
python app to run kafka cli 
first create topic with this schema 
```
{
  "type": "record",
  "name": "ProductRecord",
  "fields": [
    {"name": "ID", "type": "int"},
    {"name": "Product", "type": "string"},
    {"name": "Customer", "type": "string"},
    {"name": "Quantity", "type": "int"}
  ]
}
```
modify the Python code and put your information in this filed <topic_name> <schema_id>
## run kafka CLI Container :
Navigate to the directory where you have saved the Docker Compose file, 
and run this command to get the network name that we use:
```
docker network ls
```
you will get an output like this:
```
NETWORK ID     NAME                    DRIVER    SCOPE
98842623c91b   bridge                  bridge    local
93b3993c71bc   cp-all-in-one_default   bridge    local
1a3f2ff21715   host                    host      local
5059222addc0   none                    null      local
```
copy the network name and past it in this command after (network=) like this:

```
docker run --rm -it --network=cp-all-in-one_default confluentinc/cp-kafka-connect bash
```
## After the container run: 
copy the container name and pest it into <container name> in the Python file 
