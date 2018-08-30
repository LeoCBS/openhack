To deploy this frond-end app into a public endpoint, we used [Azure webapp service](https://azure.microsoft.com/en-us/services/app-service/web/).  
With you azure-cli configured for your desired subscription, make sure to set up the webapp extension:
```sh
az extension add -n webapp
``` 

Then deploy this app from inside `client` folder runing:
```sh
az webapp up -n minecraft-server-manager
```

There should be created a pulic URL for you to access it like:  
[minecraft-server-manager.azurewebsites.net](https://minecraft-server-manager.azurewebsites.net)
