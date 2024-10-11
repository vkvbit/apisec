import argparse
import sys
import json
from . import rest, soap, graphql, init


def main():
    parser = argparse.ArgumentParser(
        description="API Security Testing Tool"
    )

    parser.add_argument(
        "-bs",
        "--basic-scan",
        type=str,
        help="Domain name for basic scan"
    )

    parser.add_argument(
        "-ae",
        "--advanced-endpoint",
        type=str,
        help="Endpoint for advanced scan"
    )

    parser.add_argument(
        "-ah",
        "--advanced-headers",
        type=str,
        help="Header for advanced scan"
    )

    parser.add_argument(
        "-su",
        "--swagger-url",
        type=str,
        help="Swagger URL"
    )

    parser.add_argument(
        "-sf",
        "--swagger-file",
        type=str,
        help="Swagger file"
    )

    parser.add_argument(
        "-s",
        "--soap",
        type=str,
        help="SOAP endpoint"
    )

    parser.add_argument(
        "-g",
        "--graphql",
        type=str,
        help="GraphQL endpoint"
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Save output to file in JSON format"
    )

    parser.add_argument(
        "-i",
        "--init",
        action="store_true",
        help="Initialize the tool and install dependencies"        
    )

    args = parser.parse_args()

    if args.init:
        init.setup()

    if args.basic_scan:
        basic_scan_result = rest.run_basic_scan(args.basic_scan, None)
        if args.output:
            with open(args.output, 'w') as file:
                file.write(json.dumps(basic_scan_result, indent=2))
        else:
            print(json.dumps(basic_scan_result, indent=2))

    if args.advanced_endpoint and args.advanced_headers:
        advanced_scan_result = rest.run_advanced_tool(args.advanced_endpoint, args.advanced_headers)
        if args.output:
            with open(args.output, 'w') as file:
                file.write(json.dumps(advanced_scan_result, indent=2))
        else:
            print(json.dumps(advanced_scan_result, indent=2))

    if args.swagger_file and args.swagger_url:
        swagger_result = rest.run_swagger(args.swagger_file, args.swagger_url)
        if args.output:
            with open(args.output, 'w') as file:
                file.write(json.dumps(swagger_result, indent=2))
        else:
            print(json.dumps(swagger_result, indent=2))

    if args.soap:
        soap_result = soap.zap_soap(args.soap)
        if args.output:
            with open(args.output, 'w') as file:
                file.write(json.dumps(soap_result, indent=2))
        else:
            print(json.dumps(soap_result, indent=2))

    if args.graphql:
        graphql_result = graphql.scan_graphql(args.graphql)
        if args.output:
            with open(args.output, 'w') as file:
                file.write(json.dumps(graphql_result, indent=2))
        else:
            print(json.dumps(graphql_result, indent=2))

if __name__ == '__main__':
    main()
