import yaml
import time
from random import randint

from os import path
from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Configs can be set in Configuration class directly or using helper utility
#print("loading kube config")
#config.load_kube_config()

#v1 = client.CoreV1Api()
#print("Listing pods with their IPs:")
#ret = v1.list_pod_for_all_namespaces(watch=False)
#for i in ret.items:
#    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

def create_minecraft_deployment(name):
    deployment = create_deployment_object(name)
    config.load_kube_config()
    api_instance = client.ExtensionsV1beta1Api()
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace="default")
    print("Deployment created. status='%s'" % str(api_response.status))

def create_deployment_object(name):
    # Configureate Pod template container
    container = client.V1Container(
        name="minecraft",
        image="openhack/minecraft-server:2.0",
        ports=[client.V1ContainerPort(container_port=25565),client.V1ContainerPort(container_port=25575)],
        volume_mounts=[client.V1VolumeMount(name="volume", mount_path="/data")],
        env=[client.V1EnvVar(name="EULA", value="true")])
    volumes = client.V1Volume(
        name="volume", persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(claim_name="azure-managed-disk"))
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(containers=[container], volumes=[volumes]))
    # Create the specification of deployment
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=1,
        template=template)
    # Instantiate the deployment object
    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec)

    return deployment

def create_service(name):
    config.load_kube_config()
    api_instance = client.CoreV1Api()
    namespace = 'default'

    manifest = {
        "kind": "Service",
        "apiVersion": "v1",
        "metadata": {
            "name": name
        },
        "spec": {
            "selector": {
                "app": name
            },
            "ports": [
                {
                    "protocol": "TCP",
                    "port": 25565,
                    "targetPort": 25565,
                    "name": "server"
                },
                {
                    "protocol": "TCP",
                    "port": 25575,
                    "targetPort": 25575,
                    "name": "rcon"
                }
            ],
            "type": "LoadBalancer"
        }
    }

    try:
        api_response = api_instance.create_namespaced_service(namespace, manifest, pretty=True)
        print(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->create_namespaced_endpoints: %s\n" % e)

def get_service(name, logger):
    while True:
        try:
            config.load_kube_config()
            api_instance = client.CoreV1Api()
            resp = api_instance.read_namespaced_service(name=name, namespace='default')
            ip = resp.status.load_balancer.ingress[0].ip
            logger.info("service ip {}".format(ip))
            return ip
        except:
            logger.info("empty IP, trying again")
            time.sleep(5)

def create_minecraft_server(logger):
    name = "minecraft-{}".format(randint(0, 9999))
    logger.info('creating deployment')
    create_minecraft_deployment(name)
    logger.info('creating service')
    create_service(name)
    ip = get_service(name, logger)
    logger.info('got this server IP {}'.format(ip))
    respJson = {"name": name, "endpoints": {"minecraft": "{}:{}".format(ip, "22565"), "rcon": "{}:{}".format(ip, "22575")}}
    return str(respJson)