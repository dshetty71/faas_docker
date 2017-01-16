docker service create --mount type=volume,target=/usr/share/elasticsearch/data --constraint node.hostname==node3 --name elasticsearch -p 9200:9200 elasticsearch:2.4.0

docker service create --name kibana -e ELASTICSEARCH_URL="http://192.168.1.6:9200" -p 5601:5601 kibana:4.6.0

docker service create --mode global --name cadvisor --mount type=bind,source=/,target=/rootfs,readonly=true --mount type=bind,source=/var/run,target=/var/run,readonly=false --mount type=bind,source=/sys,target=/sys,readonly=true --mount type=bind,source=/var/lib/docker/,target=/var/lib/docker,readonly=true google/cadvisor:latest -storage_driver=elasticsearch -storage_driver_es_host="http://192.168.1.6:9200"

Execute this on manager or any node:

curl -X PUT http://192.168.1.6:9200/.kibana/index-pattern/cadvisor -d '{"title" : "cadvisor",  "timeFieldName": "container_stats.timestamp"}'

Update Kibana dashboard with settings:

Goto http://192.168.1.7:5601(Identify IP of the node running Kibana and access it)
Goto setting tab and select Objects and import JSON Settings for Kibana file
























































































































































































































































































































































