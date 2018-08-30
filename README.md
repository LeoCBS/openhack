# openhack
This is our solution to Microsoft's OpenHack challanges

## Minecraft Server Management API
POST /create → `empty body`  
└── 200 OK
```json
{
    "name": "tenant1",
    "endpoints": {
      "minecraft": "128.124.90.15:25565",
      "rcon": "128.124.90.15:25575"
    }
}
```

GET /list  
└── 200 OK
```json
[
  {
    "name": "tenant1",
    "endpoints": {
      "minecraft": "128.124.90.15:25565",
      "rcon": "128.124.90.15:25575"
    }
  },
  {
    "name": "tenant2",
    "endpoints": {
      "minecraft": "128.194.90.16:25565",
      "rcon": "128.194.90.16:25575"
    }
  },
  {
    "name": "tenant3",
    "endpoints": {
      "minecraft": "128.194.90.16:25566",
      "rcon": "128.194.90.16:25576"
    }
  }
]
```

DELETE /:name  
└── 200 OK
```json
{"message": "Server :name deleted"}
```