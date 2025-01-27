import subprocess
import sys
import json
import requests
import argparse

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        Namespace: Parsed arguments containing podname and output.
    """
    parser = argparse.ArgumentParser(description="Scan Docker Images with Trivy")
    parser.add_argument("--podname", required=True, help="Name of the Docker image to scan")
    parser.add_argument("--output", required=False, default="scan_results.json", help="Output file to store scan results")
    #parser.add_argument("--slack_webhook", required=False, help="Slack webhook URL for notifications")
    return parser.parse_args()

def scan_docker_image(image_name):
    """
    Scan a Docker image using Trivy and return scan results.

    Args:
        image_name (str): The name of the Docker image to scan.

    Returns:
        dict: Trivy scan results in JSON format.
    """
    try:
        print(f"Scanning Docker image: {image_name} using Trivy...")
        command = ["trivy", "image", "--format", "json", image_name]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        scan_results = json.loads(result.stdout)
        return scan_results

    except subprocess.CalledProcessError as e:
        print(f"Error during scanning: {e.stderr}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding Trivy JSON output: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during scanning: {e}")
        sys.exit(1)

def save_scan_results(scan_results, output_file):
    """
    Save scan results to a file.

    Args:
        scan_results (dict): Scan results in JSON format.
        output_file (str): The file path to save the scan results.
    """
    try:
        with open(output_file, "w") as f:
            json.dump(scan_results, f, indent=4)
        print(f"Scan results saved to {output_file}")
    except Exception as e:
        print(f"Error saving scan results: {e}")
        sys.exit(1)

def send_slack_notification(webhook_url, image_name, vulnerabilities):
    """
    Send a Slack notification for critical vulnerabilities.

    Args:
        webhook_url (str): Slack webhook URL.
        image_name (str): The name of the Docker image.
        vulnerabilities (list): List of critical vulnerabilities.
    """
    if not webhook_url:
        print("Slack webhook URL is not provided.")
        return

    vulnerability_details = "\n".join([
        f"- {vuln.get('VulnerabilityID', 'N/A')}: {vuln.get('Title', 'N/A')}"
        for vuln in vulnerabilities
    ])

    message = {
        "text": (
            f":warning: *Critical Vulnerabilities Detected in Image: {image_name}*\n\n"
            f"The following critical vulnerabilities were found:\n"
            f"{vulnerability_details}"
        )
    }

    try:
        response = requests.post(webhook_url, json=message)
        if response.status_code == 200:
            print("Slack notification sent successfully.")
        else:
            print(f"Failed to send Slack notification. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending Slack notification: {e}")

def analyze_scan_results(scan_results):
    """
    Analyze scan results and return critical vulnerabilities.

    Args:
        scan_results (dict): Trivy scan results in JSON format.

    Returns:
        list: List of critical vulnerabilities found.
    """
    critical_vulnerabilities = []
    for result in scan_results.get("Results", []):
        for vulnerability in result.get("Vulnerabilities", []):
            if vulnerability.get("Severity") == "CRITICAL":
                critical_vulnerabilities.append(vulnerability)

    return critical_vulnerabilities

if __name__ == "__main__":
    args = parse_arguments()

    # Step 1: Scan the Docker image
    scan_results = scan_docker_image(args.podname)

    # Step 2: Save the scan results
    save_scan_results(scan_results, args.output)

    # Step 3: Analyze vulnerabilities and notify if critical found
    critical_vulnerabilities = analyze_scan_results(scan_results)

    if critical_vulnerabilities:
        print(f"Critical vulnerabilities found: {len(critical_vulnerabilities)}")
        #send_slack_notification(args.slack_webhook, args.podname, critical_vulnerabilities)
        sys.exit(1)
    else:
        print("No critical vulnerabilities found.")
        sys.exit(0)
