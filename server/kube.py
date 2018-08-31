import yaml
import time
from random import randint

from os import path
from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Configs can be set in Configuration class directly or using helper utility
# print("loading kube config")
# config.load_kube_config()

# v1 = client.CoreV1Api()
# print("Listing pods with their IPs:")
# ret = v1.list_pod_for_all_namespaces(watch=False)
# for i in ret.items:
#    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

NAMESPACE = "minecraft"


def create_minecraft_deployment(name):
    deployment = create_deployment_object(name)
    config.load_kube_config()
    api_instance = client.ExtensionsV1beta1Api()
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace=NAMESPACE)
    print("Deployment created. status='%s'" % str(api_response.status))


def create_deployment_object(name):
    # Configureate Pod template container
    container = client.V1Container(
        name="minecraft",
        image="openhack/minecraft-server:2.0",
        ports=[client.V1ContainerPort(
            container_port=25565), client.V1ContainerPort(container_port=25575)],
        volume_mounts=[client.V1VolumeMount(
            name="volume", mount_path="/data")],
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
        api_response = api_instance.create_namespaced_service(
            NAMESPACE, manifest, pretty=True)
        print(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->create_namespaced_endpoints: %s\n" % e)


def get_service(name, logger):
    while True:
        try:
            config.load_kube_config()
            api_instance = client.CoreV1Api()
            resp = api_instance.read_namespaced_service(
                name=name, namespace=NAMESPACE)
            ip = resp.status.load_balancer.ingress[0].ip
            logger.info("service ip {}".format(ip))
            return ip
        except:
            logger.info("empty IP, trying again")
            time.sleep(5)


def list_services(logger):
    config.load_kube_config()
    api_instance = client.CoreV1Api()
    services = api_instance.list_namespaced_service(
        namespace=NAMESPACE, watch=False)
    servers = []
    for svc in services.items:
        ip = "<pending>"
        if svc.status.load_balancer.ingress is not None:
            ip = svc.status.load_balancer.ingress[0].ip
        serv = get_server_json(svc.metadata.name, ip)
        servers.append(serv)
    logger.info("servers {}".format(servers))
    return servers


def delete_service(name, logger):
    config.load_kube_config()
    api_instance = client.ExtensionsV1beta1Api()
    body = client.V1DeleteOptions()  # V1DeleteOptions |
    # int | The duration in seconds before the object should be deleted. Value must be non-negative integer. The value zero indicates delete immediately. If this value is nil, the default grace period for the specified type will be used. Defaults to a per object value if not specified. zero means delete immediately. (optional)
    grace_period_seconds = 56
    # bool | Deprecated: please use the PropagationPolicy, this field will be deprecated in 1.7. Should the dependent objects be orphaned. If true/false, the \"orphan\" finalizer will be added to/removed from the object's finalizers list. Either this field or PropagationPolicy may be set, but not both. (optional)
    orphan_dependents = True

    try:
        api_response = api_instance.delete_namespaced_deployment(
            name,
            NAMESPACE,
            body,
            grace_period_seconds=grace_period_seconds,
            orphan_dependents=orphan_dependents,
            propagation_policy="Foreground"
        )
        logger.info("deleted deployment \n {}".format(api_response))
        api_instance = client.CoreV1Api()
        api_response = api_instance.delete_namespaced_service(
            name,
            NAMESPACE,
            body,
            grace_period_seconds=grace_period_seconds,
            orphan_dependents=orphan_dependents,
            propagation_policy="Foreground"
        )
        logger.info("deleted service \n {}".format(api_response))
        #api_response = api_instance.delete_namespaced_pod(
        #    name,
        #    NAMESPACE,
        #    body,
        #    grace_period_seconds=grace_period_seconds,
        #    orphan_dependents=orphan_dependents,
        #    propagation_policy="Foreground"
        #)
        #logger.info("deleted pod \n {}".format(api_response))
    except Exception as e:
        logger.info("Exception when calling ExtensionsV1beta1Api->delete_namespaced_deployment: {}\n".format(e))

def get_server_json(name, ip):
    return {"name": name, "endpoints": {"minecraft": "{}:{}".format(ip, "22565"), "rcon": "{}:{}".format(ip, "22575")}}

def create_minecraft_server(logger):
    name = "minecraft-{}".format(randint(0, 9999))
    logger.info('creating deployment')
    create_minecraft_deployment(name)
    logger.info('creating service')
    create_service(name)
    ip = get_service(name, logger)
    logger.info('got this server IP {}'.format(ip))
    respJson = {"name": name, "endpoints": {"minecraft": "{}:{}".format(ip, "22565"), "rcon": "{}:{}".format(ip, "22575")}}
    return respJson
