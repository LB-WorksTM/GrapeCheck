import subprocess

import re

import sys

import os

import requests



# Enable ANSI escape sequences on Windows

os.system('')



GREEN = "\033[92m"

RED = "\033[91m"

YELLOW = "\033[93m"

CYAN = "\033[96m"

RESET = "\033[0m"



# ==========================================

# JAVA FUNCTIONS

# ==========================================



def get_latest_online_java_version():

    """Fetches the latest General Availability release version for Java 8 (1.8) from Adoptium."""

    try:

        # Targets the version range [8,9) to isolate Java 8 updates

        url = "https://api.adoptium.net/v3/assets/feature_releases/8/ga?image_type=jdk&project=jdk&sort_method=DATE&sort_order=DESC&page_size=1"

        response = requests.get(url, timeout=5)

        if response.status_code == 200:

            data = response.json()

            if data and isinstance(data, list) and len(data) > 0:

                return data[0]["version_data"]["openjdk_version"]

    except Exception:

        pass

    return None



def get_local_java_version():

    try:

        result = subprocess.run(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        output = result.stderr

        

        match = re.search(r'"([^"]+)"', output)

        if match:

            return match.group(1)

    except FileNotFoundError:

        return "Not Installed"

    return None



def normalize_java_version(version_str):

    """

    Extracts the update version number specifically for Java 8 / 1.8.

    Examples: 

      "1.8.0_452" -> 452

      "8u492-b09" -> 492

    """

    if not version_str or version_str == "Not Installed":

        return 0

        

    # Handle classic "1.8.0_XXX" formats

    if "1.8.0_" in version_str:

        match = re.search(r'1\.8\.0_([0-9]+)', version_str)

        if match:

            return int(match.group(1))

            

    # Handle OpenJDK "8uXXX" formats

    match = re.search(r'8u([0-9]+)', version_str)

    if match:

        return int(match.group(1))



    # Fallback to look for any trailing trailing digits if format varies

    match = re.search(r'([0-9]+)$', version_str)

    if match:

        return int(match.group(1))

        

    return 0



# ==========================================

# PYTHON FUNCTIONS

# ==========================================



def get_latest_online_python_version():

    """Fetches the latest stable Python version from endoflife.date API."""

    try:

        url = "https://endoflife.date/api/python.json"

        response = requests.get(url, timeout=5)

        if response.status_code == 200:

            data = response.json()

            if data and isinstance(data, list):

                return data[0]["latest"]

    except Exception:

        pass

    return None



def get_local_python_version():

    """Gets the current running Python version tuple and standard string format."""

    v = sys.version_info

    return (v.major, v.minor, v.micro), f"{v.major}.{v.minor}.{v.micro}"



def parse_version_string(version_str):

    """Converts a version string 'X.Y.Z' into a tuple of integers for accurate comparison."""

    try:

        return tuple(map(int, version_str.split('.')))

    except Exception:

        return (0, 0, 0)



# ==========================================

# MAIN EXECUTION

# ==========================================



def main():

    # --------------------------------------

    # 1. JAVA CHECK

    # --------------------------------------

    print()

    print(f"               {CYAN}JAVA (1.8 Line){RESET}")

    

    raw_local_java = get_local_java_version()

    if raw_local_java == "Not Installed":

        print(f"{RED}[ERROR] Java is not installed or not found in your system environment PATH.{RESET}")

    else:

        # Check if local installation is actually Java 8

        if "1.8." not in raw_local_java and not raw_local_java.startswith("8u"):

            print(f"{YELLOW}[WARNING] Your local Java version ({raw_local_java}) is not part of the 1.8 release line.{RESET}")

            

        local_java_update = normalize_java_version(raw_local_java)

        print(f"Your Installed Java:     Version {YELLOW}{raw_local_java}{RESET} (Update: {local_java_update})")

        

        raw_online_java = get_latest_online_java_version()

        if not raw_online_java:

            print(f"{YELLOW}[WARNING] Could not fetch Java 1.8 data from the internet.{RESET}")

        else:

            online_java_update = normalize_java_version(raw_online_java)

            print(f"Latest Online Release:   Version {YELLOW}{raw_online_java}{RESET} (Update: {online_java_update})")

            

            if local_java_update < online_java_update:

                print(f"[STATUS] {RED}OUT OF DATE.{RESET} You are behind the latest public 1.8 update (u{online_java_update}).")

            elif local_java_update > online_java_update:

                print(f"[STATUS] {GREEN}UP TO DATE.{RESET} You are running a cutting edge/custom update version (u{local_java_update}).")

            else:

                print(f"[STATUS] {GREEN}UP TO DATE.{RESET} Your local update patch matches the newest public 1.8 standard.")

    

    # --------------------------------------

    # 2. PYTHON CHECK

    # --------------------------------------

    print()

    print(f"                   {CYAN}PYTHON{RESET}")

    

    local_py_tuple, local_py_str = get_local_python_version()

    print(f"Your Installed Python:   Version {YELLOW}{local_py_str}{RESET}")

    

    raw_online_python = get_latest_online_python_version()

    if not raw_online_python:

        print(f"{YELLOW}[WARNING] Could not fetch Python data from the internet.{RESET}")

    else:

        online_py_tuple = parse_version_string(raw_online_python)

        print(f"Latest Online Release:   Version {YELLOW}{raw_online_python}{RESET}")

        

        if local_py_tuple < online_py_tuple:

            print(f"[STATUS] {RED}OUT OF DATE.{RESET} A newer stable release ({raw_online_python}) is available.")

        elif local_py_tuple > online_py_tuple:

            print(f"[STATUS] {GREEN}UP TO DATE.{RESET} You are running a newer/pre-release build ({local_py_str}).")

        else:

            print(f"[STATUS] {GREEN}UP TO DATE.{RESET} Your Python version is completely up to date.")



    input("\nPress Enter to exit...")



if __name__ == "__main__":

    main() 