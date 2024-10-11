import xml.etree.ElementTree as ET
import os
import json
import subprocess
import re



def api_discovery(domain, extra):
    if extra == False:
        gobuster_cmd = f"gobuster dir -e -u https://{domain} -t 50 -o gobuster.txt -w ./raft-small-directories.txt"
        wfuzz_get = f"wfuzz -f wfuzz_get,magictree -w ./raft-small-directories.txt --sc 200,201,202,203,300,400,401 -X GET https://{domain}/FUZZ"
        wfuzz_post = f"wfuzz -f wfuzz_post,magictree -w ./raft-small-directories.txt --sc 200,201,202,203,300,400,401 -X POST https://{domain}/FUZZ"
    else:
        gobuster_cmd = f"gobuster -e -u https://{domain} -t 50 -o gobuster.txt -w ./raft-small-directories.txt"
        wfuzz_get = f"wfuzz -f wfuzz_get,magictree -w ./raft-small-directories.txt --sc 200,201,202,203,300,400,401 -X GET https://{domain}/{extra}/FUZZ"
        wfuzz_post = f"wfuzz -f wfuzz_post,magictree -w ./raft-small-directories.txt --sc 200,201,202,203,300,400,401 -X POST https://{domain}/{extra}/FUZZ"
         
    os.system(gobuster_cmd)
    os.system(wfuzz_get)
    os.system(wfuzz_post)


def aggregate_endpoints():
    urls = []

    try:
        gobuster_pattern = r'https?://[^\s]+'
        with open("gobuster.txt", 'r') as gobuster_file:
            data = gobuster_file.readlines()
            for line in data:
                found_urls = re.findall(gobuster_pattern, line)
                urls.extend(found_urls)
    except:
        pass

    try:
        with open("wfuzz_get", 'r') as wfuzz_get_file:
            data_get = wfuzz_get_file.read()
            get_root = ET.fromstring(data_get)
            get_urls = [url.text.strip() for url in get_root.findall(".//url")]
            urls.extend(get_urls)
    except:
        pass

    try:
        with open("wfuzz_post", 'r') as wfuzz_post_file:
            data_post = wfuzz_post_file.read()
            post_root = ET.fromstring(data_post)
            post_urls = [url.text.strip() for url in post_root.findall(".//url")]
            urls.extend(post_urls)
    except:
        pass

    with open("all_urls.json", 'w') as all_urls_file:
        all_urls_file.write(json.dumps(urls))
    
    if os.path.exists("gobuster.txt"):
        os.remove("gobuster.txt")
    if os.path.exists("wfuzz_get"):
        os.remove("wfuzz_get")
    if os.path.exists("wfuzz_post"):
        os.remove("wfuzz_post")

    return urls

def basic_tool(urls):
    formatted_data = []

    for url in urls:
        wapiti_cmd = f"wapiti  -u {url} -f json -o wapiti.json"
        wapiti_result = subprocess.run(wapiti_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        with open("wapiti.json", 'r') as wapiti_file:
            data = wapiti_file.read()
            
        vulns = []

        if "vulnerabilities" in data:
            for vulnerability, value in data["vulnerabilities"].items():
                if value:
                    for vul in value:
                        vuln = {
                            "alert": vulnerability,
                            "desc": vul.get("info", ""),
                            "evidence": vul.get("http_request", ""),
                            "trigger": vul.get("curl_command", ""),
                            "vulnerable": True, 
                            "misc_data": {
                                "severity": vul.get("level", "")
                            }
                        }
                        vulns.append(vuln)

        url = data.get("infos", {}).get("target", "")

        url_vulns = {
            "url": url,
            "vulns": vulns
        }

        formatted_data.append(url_vulns)
    return formatted_data

def run_basic_scan(domain, extra):

    api_discovery(domain, extra)

    urls = aggregate_endpoints()

    with open("all_urls.json", 'r') as all_urls_file:
        urls = json.loads(all_urls_file.read())

    api_vulns = basic_tool(urls)

    return api_vulns

 








def run_advanced_tool(endpoint, headers=None):

    if headers:
        headers_cmd = " ".join([f"-H '{h}'" for h in headers])
    else:
        headers_cmd = ""

    wapiti_cmd = f"wapiti -u {endpoint} {headers_cmd} -f json -o wapiti_adv.json"
    wapiti_result = subprocess.run(wapiti_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if wapiti_result.returncode != 0:
        return {
            "error": "Wapiti scan failed",
            "details": wapiti_result.stderr.decode('utf-8')
        }

    try:
        with open("wapiti_adv.json", 'r') as wapiti_file:
            wapiti_data = json.load(wapiti_file)
    except FileNotFoundError:
        return {"error": "Wapiti result file not found"}
    except json.JSONDecodeError:
        return {"error": "Failed to decode Wapiti JSON output"}

    formatted_data = []
    vulns = []

    if "vulnerabilities" in wapiti_data:
        for vulnerability, value in wapiti_data["vulnerabilities"].items():
            if value:
                for vul in value:
                    vuln = {
                        "alert": vulnerability,
                        "desc": vul.get("info", ""),
                        "evidence": vul.get("http_request", ""),
                        "trigger": vul.get("curl_command", ""),
                        "vulnerable": True, 
                        "misc_data": {
                            "severity": vul.get("level", "")
                        }
                    }
                    vulns.append(vuln)

    url = wapiti_data.get("infos", {}).get("target", "")

    url_vulns = {
        "url": url,
        "vulns": vulns
    }

    formatted_data.append(url_vulns)

    if os.path.exists("wapiti_adv.json"):
        os.remove("wapiti_adv.json")

    return formatted_data




def run_swagger(swagger_file, endpoint):
    offat_cmd = f"python3 -m offat -f {swagger_file} --server {endpoint} -o offat.json -of json"
    
    offat_result = subprocess.run(offat_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("stdout:", offat_result.stdout.decode())
    print("stderr:", offat_result.stderr.decode())
    
    if offat_result.returncode != 0:
        raise Exception("Failed to run offat command")

    if not os.path.exists("offat.json"):
        raise FileNotFoundError("The file 'offat.json' was not created.")
    
    with open("offat.json", 'r') as offat_file:
        data = json.load(offat_file)

    formatted_data = []
    url_vulns = {}

    for result in data['results']:
        url = result["url"]  
        if result.get("vulnerable", False):
            if url not in url_vulns:
                url_vulns[url] = {
                    "url": url,
                    "vulns": []
                }
            vuln = {
                "alert": result["test_name"],  
                "desc": result.get("vuln_details", ""),
                "evidence": result.get("data_leak", ""),
                "trigger": result.get("malicious_payload", []),
                "vulnerable": True,
                "misc_data": {
                    "reference": result.get("response_body", ""),
                }
            }
            url_vulns[url]["vulns"].append(vuln)
    
    formatted_data = list(url_vulns.values())

    os.remove("offat.json")

    return formatted_data