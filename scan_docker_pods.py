import subprocess
import os
import sys
import json
import requests
import argparse
PROMETHEUS_PUSHGATEWAY = "http://192.168.1.14:9090/"
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
    push_to_prometheus(image_name, critical_count, high_count)
    #response = requests.post(webhook_url, json=message)
    print (response)
    if response.status_code == 200:
        print("Slack notification sent successfully.")
    else:
        print(f"Failed to send Slack notification. Status code: {response.status_code}")

def push_to_prometheus(image_name, critical, high):
    metric_data = f"""
    # HELP docker_scan_critical_count Number of critical vulnerabilities
    # TYPE docker_scan_critical_count gauge
    docker_scan_critical_count{{image_name="{image_name}"}} {critical}

    # HELP docker_scan_high_count Number of high vulnerabilities
    # TYPE docker_scan_high_count gauge
    docker_scan_high_count{{image_name="{image_name}"}} {high}
    """
    requests.post(f"{PROMETHEUS_PUSHGATEWAY}/metrics/job/docker_scan", data=metric_data)


if __name__ == "__main__":
    #pod_name = "nginx:latest"  # Example pod name
    #output_json = "scan_results.json"
    #output_pdf = "scan_report.pdf"

    parser = argparse.ArgumentParser(description="Scan Docker Pods")
    parser.add_argument("--podname", required=True, help="Name of the pod to scan")
    args = parser.parse_args()
    pod_name = args.podname
    output = pod_name+".json"
    PDF_output = pod_name+".pdf"
    status = 1

    slack_webhook_url = "https://hooks.slack.com/services/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"

    # Step 1: Scan the Docker pod
    scan_results = scan_docker_pod(pod_name)

    # Step 2: Generate the PDF report
    generate_pdf_from_json(scan_results, output_pdf)

    # Step 3: Check for critical vulnerabilities and send Slack notification
    critical_vulnerabilities = []
    for result in scan_results.get("Results", []):
        for vulnerability in result.get("Vulnerabilities", []):
            if vulnerability.get("Severity") == "CRITICAL":
                critical_vulnerabilities.append(vulnerability)

    if critical_vulnerabilities:
        send_slack_notification(slack_webhook_url, pod_name, critical_vulnerabilities)
        sys.exit(1)
    else:
        print("No critical vulnerabilities found.")
        sys.exit(0)

