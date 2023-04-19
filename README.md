az acr login --name az4registry.azurecr.io

docker context ls
docker context use default

docker build -t producer:latest -f .\producer\Dockerfile .
docker images

docker login az4registry.azurecr.io

docker tag producer:latest az4registry.azurecr.io/producer
docker images

docker push az4registry.azurecr.io/producer
--------------------------------------------
# PULLING IMAGE FROM AZURE CONTAINER REGISTRY
# docker should be running
# https://learn.microsoft.com/en-us/azure/container-registry/container-registry-auth-kubernetes
az acr login -n az4registry --expose-token
or
az acr login --name az4registry.azurecr.io

kubectl create secret docker-registry <secret-name> \
    --namespace <namespace> \
    --docker-server=<container-registry-name>.azurecr.io \
    --docker-username=<service-principal-ID> \
    --docker-password=<service-principal-password>

1. secret-name = acr-secret
2. namespace = default
3. container-registry-name = az4registry
# (ID of the service principal that will be used by Kubernetes to access your registry)
4. service-principal-ID = az4registry 
5. service-principal-password = 6CbHuf2bdRBxzQjipoTdm2DXtSzYnAU5MBtcYyy0W3+ACRBfbjVB

# CREATE SECRET KEY FOR ACR 
kubectl create secret docker-registry acr-secret --docker-server=az4registry.azurecr.io --docker-username=az4registry --docker-password=6CbHuf2bdRBxzQjipoTdm2DXtSzYnAU5MBtcYyy0W3+ACRBfbjVB

=======================================
# CREATE SECRET KEY FOR DOCKER-HUB

Step by step how to pull a private DockerHub hosted image in a Kubernetes YML.

export DOCKER_REGISTRY_SERVER=https://index.docker.io/v1/
export DOCKER_USER=Type your dockerhub username, same as when you `docker login`
export DOCKER_EMAIL=Type your dockerhub email, same as when you `docker login`
export DOCKER_PASSWORD=Type your dockerhub pw, same as when you `docker login`

kubectl create secret docker-registry myregistrykey \
  --docker-server=$DOCKER_REGISTRY_SERVER \
  --docker-username=$DOCKER_USER \
  --docker-password=$DOCKER_PASSWORD \
  --docker-email=$DOCKER_EMAIL

kubectl create secret docker-registry dochub-secret --docker-server=https://index.docker.io/v1/ --docker-username=soumya.pdit@gmail.com --docker-password=Soumyajeevan33 --docker-email=soumya.pdit@gmail.com

===================================

Steps to create topic via commandline : (assumed zookeeper running on port 2181 and kafka server on 9092)

Get inside the kafka pod by using this command
kubectl exec -it kafka-pod-name -- /bin/bash

Create the topic by using below command
kafka-topics --bootstrap-server localhost:9092 --create --topic topic-name --replication-factor 1 --partitions 3

you can verify the message produce and consume using below commands-
a) produce-->

kafka-console-producer --broker-list localhost:9092 --topic <topic-you-created-before>
provide some message
b) consume--> kafka-console-consumer --bootstrap-server localhost:9092 --topic audit --from-beginning

=========================================================

video:
https://www.youtube.com/watch?v=rPU6YKKWZ1c
https://github.com/skshukla/KubernetesSample/tree/dev-infra/kafka

kafka:
https://kow3ns.github.io/kubernetes-kafka/manifests/

zookeeper:
https://github.com/kow3ns/kubernetes-zookeeper/tree/master/manifests

# ----------------------------------
# KUBERNETES COMMANDS

# WATCH
kubectl get svc,deployments,statefulset,pods,pv,pvc -o wide --show-labels -l app=kafka

kubectl get pod -w
kubectl get pod -l 'app=kafka'
kubectl describe pod/kafka-d-0-0

kubectl delete pod/zookeeper-0 pod/kafka-d-0-0 pod/kafka-d-0-1

kubectl create -f ka.yml

# LOGS
kubectl logs <pod-name>

# EXECUTION
kubectl exec -it <pod-name> -- /bin/bash

# ZOOKEEPER zkCli.sh
kubectl exec -it zookeeper-0 -- /bin/bash
cd /opt/zookeeper/bin
ls
#
zkCli.sh -server <kafka-pod-NODE-ip>:30003  # aks-agentpool-25111405-vmss000000
or
zkCli.sh -server zookeeper-service.default.svc.cluster.local:2181  # client port
or 
 zkCli.sh -server zookeeper-service:2181
 #
ls/
ls /
# o/p: [cluster, controller_epoch, controller, brokers, zookeeper, admin, isr_change_notification, consumers, config]

ls /brokers
# o/p: [ids, topics, seqid]

ls /brokers/topics
# []

ls /brokers/ids
# 
# ---------------------

# TOPIC 
bin/kafka-topics.sh --zookeeper zookeeper-service:2181 --create --topic my-topic --replication-factor 1 --partitions 3

# PRODUCER-CONSOLE
bin/kafka-console-producer.sh --broker-list <kafka-ss-0-0 or pod-ip>:30092 --topic my-topic
bin/kafka-console-producer.sh --broker-list kafka-ss-0-0:30092 --topic my-topic

bin/kafka-console-consumer.sh --bootstrap-server 10.244.0.45:30092 --topic my-topic --from-beginning  # <kafka-pod-ip>

# RUN PRODUCER ON EXTERNALLY
kubectl run producer --rm --tty -i --image az4registry.azurecr.io/producer:latest --image-pull-policy Never --restart Never --namespace kafkaplaypen --command -- python3 -u ./producer.py

# RUN CONSUMER
kubectl run consumer --rm --tty -i --image az4registry.azurecr.io/consumer:latest --image-pull-policy Never --restart Never --namespace kafkaplaypen --command -- python3 -u ./consumer.py



======================

function delete() {
    eval $(minikube docker-env)
    kubectl delete svc kafka-0 kafka-1 kafka-2 || true;
    kubectl delete statefulset kafka-d-0 kafka-d-1 kafka-d-2
    kubectl delete pvc kafka-data-kafka-d-0-0 kafka-data-kafka-d-1-0 kafka-data-kafka-d-2-0
}


o do so, add the following environment variables to your docker-compose:

    environment:
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
      - ALLOW_PLAINTEXT_LISTENER=yes
+     - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
+     - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,PLAINTEXT_HOST://:29092
+     - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092

And expose the extra port:

    ports:
      - '9092:9092'
+     - '29092:29092'


and access it by 'localhost:29092' not 'localhost:9092' in your python-kafka code.

# ----------
kafdrop:
    image: obsidiandynamics/kafdrop
    ports:
      - "9000:9000"
    environment:
      KAFKA_BROKERCONNECT: localhost:9092
      JVM_OPTS: "-Xms16M -Xmx48M -Xss180K -XX:-TieredCompilation -XX:+UseStringDeduplication"
    depends_on:
      - kafka
    networks:
      - monitor-net