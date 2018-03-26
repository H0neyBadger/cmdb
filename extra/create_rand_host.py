import requests 
import json
import random 
import uuid

login="test"
password="P@ssword"

with open("dict", 'r', encoding="latin-1") as words :
     a = words.readlines()

headers = {
    'Content-type': 'application/json', 
    'Accept': 'application/json'
}

def gen_ip():
    a = random.randint(1, 254)
    b = random.randint(1, 254)
    c = random.randint(1, 254)
    d = random.randint(1, 254)
    #mask = random.randint(1, 32)
    ip_s = "{}.{}.{}.{}".format(a,b,c,d)
    return {'ip' : ip_s}
    
def gen_interface():
    name = random.choice(a).replace('\n','')
    n_int = random.randint(1, 2)
    n_ip = random.randint(1, 3)
    interfaces = []
    for i in range(n_int):
        ips = []
        for y in range(n_ip):
            ips.append(gen_ip())

        mac = ':'.join(("%12x" % random.randint(0, 0xFFFFFFFFFFFF))[i:i+2] for i in range(0, 12, 2))
        interfaces.append({
            "ip_address": ips,
            "name": "{}{}".format(name,i),
            "mac_address": mac,
            #"host": null
        })
    return interfaces

while(1):
    name = random.choice(a).replace('\n','')
    #name = random.choice(a).replace('\n',''
    snow_id = random.randint(100000, 999999)
    machine_uuid = str(uuid.uuid4())
    interfaces = gen_interface()
    data = {
        "interfaces": interfaces,
        "name": name,
        "snow_id": snow_id,
        "uuid": machine_uuid,
        "machine_id": machine_uuid,
        "local_name": name,
        "dns_name": "{}.foo.bar".format(name),
        "vm_name": name,
        #"geo": null,
        #"team": null,
        #"domain": null,
        #"hardware_type": null,
        #"parent_host": null,
        #"os_family": null,
        #"os_distribution": null,
        #"os_distribution_version": null,
        #"system_team": null,
        #"application_team": null
    }
    r = requests.post(
        'http://localhost:8081/api/v1/inventory/hosts/', 
        auth=(login, password), 
        #headers=headers,
        json=data,
    )
    print(r.text)
