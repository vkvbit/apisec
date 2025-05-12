# `apisec` (API Security Testing Tool )

![Static Badge](https://img.shields.io/badge/made_with-Python-blue) ![Static Badge](https://img.shields.io/badge/license-MIT-blue) ![Keybase PGP](https://img.shields.io/keybase/pgp/vkvbit?style=social&logoColor=blue&labelColor=blue&color=blue&link=https%3A%2F%2Fkeybase.io%2Fvkvbit)

This tool allows you to perform security scans on various types of APIs, including REST, SOAP, and GraphQL. It provides basic and advanced scans and integrates with Swagger for automated testing.

## Features

- **Basic API Scan**: Quickly scan a domain for common security vulnerabilities.
- **Advanced Endpoint Scan**: Perform a more in-depth scan on specific API endpoints with custom headers.
- **Swagger Integration**: Scan APIs using Swagger documentation (URL or file).
- **SOAP Endpoint Testing**: Test SOAP APIs for security issues.
- **GraphQL Endpoint Testing**: Scan GraphQL APIs to detect vulnerabilities.
- **Output**: Save scan results in a JSON file for later analysis.

## Installation

### Method 1: 

Install directly using pip from PyPi:

```bash
pip install apisec
```

### Method 2:

Clone the repository and install the package using `pip`:

```bash
git clone https://github.com/yourusername/apisec-tool.git
cd apisec-tool
pip install .
```

### Post Install 
After installing apisec, run below command to install all dependecies and sync path variables.

```bash
apisec -i
```

## Usage

### REST API

- Basic Scan: Perform a basic security scan on a domain:

    ```bash
    apisec -bs "<domain name>"
    ```

- Advanced Scan: Perform an advanced scan on a specific API endpoint:

    ```bash
    apisec -ae "<API endpoint>" -ah "<headers in JSON format>"
    ```

- Using Swagger JSON File: Scan APIs based on Swagger documentation:

    ```bash
    apisec -su "<API server url>" -sf "<url or path to swagger.json file>" 
    ```

### SOAP API

- SOAP Scan: Test a SOAP API by specifying its endpoint:

    ```bash
    apisec -s "<SOAP API endpoint>
    ```

### GraphQL API

- GraphQL Scan: Test a GraphQL API for security vulnerabilities:

    ```bash
    apisec -g "<GraphQL API endpoint>"
    ```

### Saving Output

To save the scan results to a JSON file for later analysis, use the -o option:

```bash
apisec -bs "<domain name>" -o "scan_results.json"
```



## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Credits

|  Projects  |  License  |
|:----------|:---------:|
| OWASP ZAP | Apache |
| GraphQL-Cop | MIT |
| Wapiti | GPL-2 |
| Wfuzz | GPL-2 |
| Gobuster | Apache |
| Offat | MIT |

