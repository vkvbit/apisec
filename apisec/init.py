import os
import subprocess
import sys

graphql_cop_path = "/opt/graphql-cop/graphql-cop.py"
zap_path = ""

def install_graphql_cop():
    """
    Install GraphQL Cop by cloning the repository and installing its dependencies.
    """
    if not os.path.exists("/opt/graphql-cop"):
        print("Cloning GraphQL Cop repository...")
        try:
            subprocess.run(["git", "clone", "https://github.com/dolevf/graphql-cop.git", "/opt/graphql-cop"], check=True)

            print("Installing GraphQL Cop dependencies...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "/opt/graphql-cop/requirements.txt"], check=True)

            print("GraphQL Cop installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while installing GraphQL Cop: {e}")
            sys.exit(1)
    else:
        print("GraphQL Cop is already installed.")

def find_zap_path():
    """
    Find the ZAP path by using the 'find' command to locate zap.sh.
    If ZAP is not found, prompt the user to install ZAP first.
    """
    print("Locating ZAP Proxy installation...")
    try:
        result = subprocess.run(['find', '/', '-name', 'zap.sh'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        zap_locations = result.stdout.decode('utf-8').strip()

        if zap_locations:
            zap_paths = zap_locations.split('\n')
            global zap_path
            zap_path = zap_paths[0]  # Use the first found location
            print(f"ZAP Proxy found at {zap_path}")
        else:
            print("ZAP Proxy not found. Please install OWASP ZAP first.")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while searching for ZAP: {e}")
        sys.exit(1)

def check_graphql_cop_path():
    """
    Check if GraphQL Cop is correctly installed and available in the expected path.
    """
    if not os.path.exists(graphql_cop_path):
        print(f"GraphQL Cop not found at {graphql_cop_path}. Please check the installation.")
        sys.exit(1)
    else:
        print(f"GraphQL Cop found at {graphql_cop_path}.")

def setup():
    """
    Perform the setup, including checking paths and installing tools.
    """
    print("Setting up GraphQL Cop and ZAP Proxy...")
    install_graphql_cop()
    find_zap_path()
    check_graphql_cop_path()
    print("=========================================")
    print("||    Setup completed successfully     ||")
    print("=========================================")
    print("You can now use the 'apisec' command to run the tool.")

