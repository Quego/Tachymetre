{
    "node": {
        "name": "gateway-node",
        "top-composer": true,
        "composition-file": "composition.js",
        "auto-start": true,
        "web-admin": 9000,
        "shell-admin": 9001     
    },
    "transport": [
        "xmpp",
        "http"
    ],
    "transport-xmpp": {
        "xmpp-port": 5222,
        "xmpp-password": "Bender",
        "xmpp-jid": "bot@charmanson.isandlatech.com",
        "xmpp-server": "charmanson.isandlatech.com"
    }
}