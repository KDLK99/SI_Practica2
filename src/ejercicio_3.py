import urllib.request
import json


def access_cve_api():
    # Se leen los datos de la web
    url = "https://cve.circl.lu/api/last/10"
    
    with urllib.request.urlopen(url) as response:
        body_json = response.read()
    # Se cargan en formato json
    body_dict = json.loads(body_json)
    
    list_strings = []
    # Se va a ir comprobando cada uno de ellos para amoldarlo a uno de los posibles formatos
    for i in range(len(body_dict)):
        
        try:
            list_strings.append(
                f"{body_dict[i]['vulnerabilities'][0]['cve']}: {body_dict[i]['vulnerabilities'][0]['cwe']['name']}\n"
                f"{body_dict[i]['vulnerabilities'][0]['notes'][1]['text']}\n")
        except:
            try:
                list_strings.append(
                    f"{body_dict[i]['cveMetadata']['cveId']}: {body_dict[i]['containers']['adp'][0]['problemTypes'][0]['descriptions'][0]['description']}\n")
            except:
                try:
                    list_strings.append(f"{body_dict[i]['cveMetadata']['cveId']}: No hay datos disponibles")
                except:
                    list_strings.append("No hay información disponible")
    return list_strings
