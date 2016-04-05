/* WARNING!: do not edit, this file is generated automatically by COHORTE startup scripts. */
{
    "import-files" : [ "boot-forker.js" ],
    "composition" : [
    {
        "name" : "pelix-http-service",
        "properties" : {
            "pelix.http.port" : 9000
        }
    }, {
        "name" : "pelix-remote-shell",
        "properties" : {
            "pelix.shell.port" : 9001
        }
    }
    ]
}
