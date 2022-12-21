### Install Kafka
```shell
helm repo add bitnami https://charts.bitnami.com/bitnami

helm install kafka-local bitnami/kafka \
--set persistence.enabled=false,zookeeper.persistence.enabled=false

kubectl run kafka-local-client \
    --restart='Never' \
    --image docker.io/bitnami/kafka:3.3.1-debian-11-r19 \
    --namespace orders-microservice \
    --command \
    -- sleep infinity

kubectl exec --tty -i kafka-local-client --namespace orders-microservice -- bash
```

### Create Topic
```shell
kafka-topics.sh  \
    --bootstrap-server kafka-local.order-microservice.svc.cluster.local:9092 \
    --create \
    --topic order-details \
    --partitions 3 \
    --replication-factor 1
    
# producer
kubectl run producer --rm --tty -i \
    --image worldbosskafka/producer:v0.0.8 \
    --restart Never \
    --namespace orders-microservice \
    --command \
    -- python3 -u ./producer.py
    
# consumer
kubectl run consumer --rm --tty -i \
    --image worldbosskafka/consumer:v0.0.9 \
    --restart Never \
    --namespace orders-microservice \
    --command \
    -- python3 -u ./consumer.py
    
# order service
kubectl run order-service --rm --tty -i \
    --image worldbosskafka/orders:v0.0.9 \
    --restart Never \
    --namespace orders-microservice \
    --command \
    -- python3 -u ./order_svc.py
    
# transaction service
kubectl run transaction-service --rm --tty -i \
    --image worldbosskafka/transactions:v0.1.0 \
    --restart Never \
    --namespace orders-microservice \
    --command \
    -- python3 -u ./consumer.py
    
# notification service
kubectl run notification-svc --rm --tty -i \
    --image worldbosskafka/notification:v0.0.9 \
    --restart Never \
    --namespace orders-microservice \
    --command \
    -- python3 -u ./notification.py
    
# analytics
kubectl run analytics-svc --rm --tty -i \
    --image worldbosskafka/analytics:v0.0.9 \
    --restart Never \
    --namespace orders-microservice \
    --command \
    -- python3 -u ./analytics.py
```

### Kakfa UI
```shell
helm repo add kafka-ui https://provectus.github.io/kafka-ui
helm install kafka-ui kafka-ui/kafka-ui \
--set envs.config.KAFKA_CLUSTERS_0_NAME=kafka-local \
--set envs.config.KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka-local.order-microservice.svc.cluster.local:9092

kubectl port-forward svc/kafka-ui 8080:8080
```

### Test Email
```shell
# PRODUCER:
kafka-console-producer.sh \
  --broker-list kafka-local-0.kafka-local-headless.orders-microservice.svc.cluster.local:9092 \
  --topic order-details 
  
b'{'order_id': '0f24aea0-1d0f-4cd7-935a-25dbc8adb1d0', 'username': 'rebecca36', 'first_name': 'Christina', 'last_name': 'Aguilar', 'email': 'theodondre@gmail.com', 'quantity': 21, 'price': 37.19, 'date_created': '2022-12-20 21:09:05.727385'}'
  

# CONSUMER:
kafka-console-consumer.sh \
  --bootstrap-server kafka-local.orders-microservice.svc.cluster.local:9092 \
  --topic order-details \
  --from-beginning

```
