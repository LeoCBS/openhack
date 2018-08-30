import yaml

from os import path
from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
print("loading kube config")
config.load_kube_config()

v1 = client.CoreV1Api()
print("Listing pods with their IPs:")
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

#with open(path.join(path.dirname(__file__), "minecraft-server.yaml")) as f:
#        dep = yaml.load(f)
#        k8s_beta = client.ExtensionsV1beta1Api()
#        resp = k8s_beta.create_namespaced_deployment(
#            body=dep, namespace="default")
#        print("Deployment created. status='%s'" % str(resp.status))