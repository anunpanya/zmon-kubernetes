import base64
import tempfile
import os
import sys
from subprocess import check_call, call

def generate_certificate(cluster_name: str):
    check = call(["which", "keytool"])
    if check:
        print("Keytool is not in searchpath")
        return

    d = tempfile.mkdtemp()
    try:
        keystore = os.path.join(d, 'keystore')
        cmd = ["keytool", "-genkeypair",
               "-alias", "planb",
               "-keyalg", "RSA",
               "-validity", "36000",
               "-keystore", keystore,
               "-dname", "c=DE, st=Berlin, l=Berlin, o=Zalando SE, cn=zalando.net",
               "-storepass", cluster_name,
               "-keypass", cluster_name]
        check_call(cmd)
        cert = os.path.join(d, 'cert')
        export = ["keytool", "-export",
                  "-alias", "planb",
                  "-keystore", keystore,
                  "-rfc",
                  "-file", cert,
                  "-storepass", cluster_name]
        check_call(export)
        truststore = os.path.join(d, 'truststore')
        importcmd = ["keytool", "-import",
                     "-noprompt",
                     "-alias", "planb",
                     "-file", cert,
                     "-keystore", truststore,
                     "-storepass", cluster_name]
        check_call(importcmd)

        with open(keystore, 'rb') as fd:
            keystore_data = fd.read()
        with open(truststore, 'rb') as fd:
            truststore_data = fd.read()
    finally:
        pass
    return keystore_data, truststore_data

k, t = generate_certificate("zmon-cassandra-01")

keystore_base64 = base64.b64encode(k)
truststore_base64 = base64.b64encode(t)

print (keystore_base64.decode("ascii"))

print ("")

print (truststore_base64.decode("ascii"))
