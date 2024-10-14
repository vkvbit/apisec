import subprocess
import json
from . import init

zap_path = init.zap_path

def zap_soap(uri):        
        
    zap_cmd_soap = f"{zap_path} -cmd -quickurl {uri} -quickout /opt/graphql-cop/zap-report.json"
    subprocess.run(zap_cmd_soap, shell=True)

    with open('/opt/graphql-cop/zap-report.json', 'r') as file:
        data = json.load(file)
    
    formatted_data = []

    url_vulns = {}

    for site in data['site']:
        for alert in site["alerts"]:
            for instance in alert["instances"]:
                uri = instance["uri"]

                if uri not in url_vulns:
                    url_vulns[uri] = []

                vuln = {
                    "alert": alert["alert"],
                    "description": alert.get("desc", ""),
                    "evidence": instance.get("evidence", ""),
                    "trigger": instance.get("attack", ""),
                    "vulnerable": True,
                    "misc_data": {
                        "risk": alert["riskdesc"],
                        "confidence": alert["confidence"],
                        "solution": alert["solution"],
                        "reference": alert["reference"],
                        "cweid": alert["cweid"],
                        "wascid": alert["wascid"],
                        "sourceid": alert["sourceid"],
                        "otherinfo": instance.get("otherinfo", ""),
                        "param": instance.get("param", ""),
                        "pluginId": alert["pluginid"],
                        "cve": alert.get("cve", ""),
                        "risk_description": alert["riskdesc"]
                    }
                }

                url_vulns[uri].append(vuln)
    if os.path.exists("/opt/graphql-cop/zap-report.json"):
        os.remove('/opt/graphql-cop/zap-report.json')

    for uri, vulns in url_vulns.items():
        formatted_data.append({
            "url": uri,
            "vulns": vulns
        })

    return formatted_data

        


