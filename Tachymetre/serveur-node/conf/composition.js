{
    "name": "tachymetre",
    "root": {
        "name": "tachymetre-composition",
        "components": [
            {
                "name"    : "cache",
                "factory" : "cache-factory",
                "node"    : "raspberry-node"
            },
            {
                "name"    : "echantillonneur",
                "factory" : "echantillonneur-factory",
                "node"    : "raspberry-node"
            },
            {
                "name"    : "elaborateur",
                "factory" : "elaborateur-factory",
                "node"    : "raspberry-node"
            },
            {
                "name"    : "sender",
                "factory" : "sender-factory",
                "node"    : "raspberry-node"
            },
            {
                "name"    : "sync",
                "factory" : "sync-factory",
                "node"    : "raspberry-node"
            },

            {
                "name"    : "aggregator",
                "factory" : "aggregator-factory",
                "node"    : "serveur-node"
            },
            {
                "name"    : "apirest",
                "factory" : "apirest-factory",
                "node"    : "serveur-node"
            },
            {
                "name"    : "interfaceutilisateur",
                "factory" : "interfaceutilisateur-factory",
                "node"    : "serveur-node"
            },
            {
                "name"    : "serveur",
                "factory" : "serveur-factory",
                "node"    : "serveur-node"
            },
        ]
    }
}
