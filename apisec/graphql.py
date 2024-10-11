import subprocess
import json
from . import init

graphql_cop_path = init.graphql_cop_path

def scan_graphql(endpoint):
    
    graphql_cmd = f"python3 {graphql_cop_path} -t {endpoint} -o json"
    
    graphql_result = subprocess.run(graphql_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    data = graphql_result.stdout.decode("utf-8")
    
    try:
        json_data = json.loads(data)  
    except json.JSONDecodeError:
        
        return {
            "url": endpoint,
            "error": "Error decoding JSON from the GraphQL command output.",
            "details": graphql_result.stderr.decode("utf-8"),  
            "vulns": []  
        }
    
    url_vulns = {
        "url": endpoint,
        "vulns": []
    }
 
    for entry in json_data:  
        if entry.get("result", False):  
            vuln = {
                "alert": entry.get("title", ""),  
                "desc": entry.get("description", ""),
                "evidence": "",  
                "trigger": entry.get("curl_verify", []),
                "vulnerable": True,
                "misc_data": {
                    "severity": entry.get("severity", ""),
                    "impact": entry.get("impact", ""),
                }
            }
            url_vulns["vulns"].append(vuln)

    return url_vulns




