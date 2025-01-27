import subprocess
import os
import sys
import json
import requests
import argparse

# Argument parsing
parser = argparse.ArgumentParser(description="Scan Docker Pods")
parser.add_argument("--podname", required=True, help="Name of the pod to scan")
parser.add_argument("--output", required=False, help="Output file to store scan results")

args = parser.parse_args()
pod_name = args.podname
output_file = args.output if args.output else "scan_results.json"

def scan_docker_pod(pod_name: str):
    """
    Scan a Docker pod using Trivy.

    Args:
        pod_name (str): The name of the Docker pod or container to scan.

    Returns:
        dict: Trivy scan results in JSON format.
    """
    try:
        print(f"Scanning pod: {pod_name} using Trivy...")
        # Run the Trivy scan command
        command = ["trivy", "image", "--format", "json", pod_name]
        result = subprocess.run(command, capture_output=True, text=True)

        # Check if the command succeeded
        if result.returncode != 0:
            print("Error occurred during scanning:")
            print(result.stderr)
            sys.exit(1)

        # Parse the JSON output
        scan_results = json.loads(result.stdout)
        return scan_results

    except Exception as e:
        print(f"An error occurred during scanning: {e}")
        sys.exit(1)

def send_slack_notification(webhook_url, pod_name, vulnerabilities):
    """
    Send a Slack notification about critical vulnerabilities.

    Args:
        webhook_url (str): Slack webhook URL.
        pod_name (str): The name of the Docker pod.
        vulnerabilities (list): List of critical vulnerabilities.
    """
    if not webhook_url:
        print("Slack webhook URL is not configured.")
        return

    vulnerability_details = "\n".join([
        f"- {vuln['VulnerabilityID']}: {vuln['Description']}"
        for vuln in vulnerabilities
    ])

    message = {
        "text": (
            f":warning: *Critical Vulnerabilities Detected in Pod: {pod_name}*\n\n"
            f"The following critical vulnerabilities were found:\n"
            f"{vulnerability_details}"
        )
    }

    response = requests.post(webhook_url, json=message)
    print (response)
    if response.status_code == 200:
        print("Slack notification sent successfully.")
    else:
        print(f"Failed to send Slack notification. Status code: {response.status_code}")


if __name__ == "__main__":


    pod_name = args.podname
    output = output_file
    status = 1

    #slack_webhook_url = "https://hooks.slack.com/services/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"

    # Step 1: Scan the Docker pod
    scan_results = scan_docker_pod(pod_name)

    # Step 3: Check for critical vulnerabilities and send Slack notification
    critical_vulnerabilities = []
    for result in scan_results.get("Results", []):
        for vulnerability in result.get("Vulnerabilities", []):
            if vulnerability.get("Severity") == "CRITICAL":
                critical_vulnerabilities.append(vulnerability)

    if critical_vulnerabilities:
        #send_slack_notification(slack_webhook_url, pod_name, critical_vulnerabilities)
        sys.exit(1)
    else:
        print("No critical vulnerabilities found.")
        sys.exit(0)
