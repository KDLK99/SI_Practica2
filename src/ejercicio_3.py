import urllib.request
import json


def access_cve_api():
    # Acceder a la web
    url = "https://cve.circl.lu/api/last/10"
    # Abrir la url y leer la respuesta
    with urllib.request.urlopen(url) as response:
        body_json = response.read()
    # Cargar el json
    body_dict = json.loads(body_json)
    # Recoger los resultados con el formato correcto y enviarlos a la web
    list_strings = []
    for i in range(len(body_dict)):
        # Intentar con diferentes formatos de texto por si alguno falla
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
