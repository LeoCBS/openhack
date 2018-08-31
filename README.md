# openhack
This is our solution to Microsoft's OpenHack challanges

## Minecraft Server Manager Webapp
We developed an app that manages to create, list and delete minecraft servers
into our Kubernetes cluster automatically.

We deployed a simple front-end at [minecraft-server-manager.azurewebsites.net](http://minecraft-server-manager.azurewebsites.net) and there is available the [Open API specication](https://app.swaggerhub.com/apis/LeoCBS/openhack/1.0.0) too.


## How create one cluster on Azure (AKS)

    az aks create --resource-group team9 --name team9-aks --node-count 1 --enable-addons monitoring --generate-ssh-keys
    az aks get-credentials --resource-group team9 --name team9-aks

## Deploy open hack server

    kubectl apply -f deploy/openhack-server/

## Deploy PersistemVolumeClain

    kubectl apply -f deploy/minecraft-server

