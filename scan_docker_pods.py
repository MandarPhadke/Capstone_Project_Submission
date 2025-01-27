import subprocess
import sys
import json
import argparse
import time
from prometheus_client import start_http_server, Gauge

# Prometheus metrics setup
CRITICAL_VULN_GAUGE = Gauge('docker_critical_vulnerabilities', 'Number of critical vulnerabilities found', ['image'])

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        Namespace: Parsed arguments containing podname and output.
    """
    parser = argparse.ArgumentParser(description="Scan Docker Images with Trivy")
    parser.add_argument("--podname", required=True, help="Name of the Docker image to scan")
    parser.add_argument("--output", required=False, default="scan_results.json", help="Output file to store scan results")
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

def analyze_scan_results(scan_results, image_name):
    """
    Analyze scan results and update Prometheus metrics.

    Args:
        scan_results (dict): Trivy scan results in JSON format.
        image_name (str): The Docker image name being analyzed.

    Returns:
        list: List of critical vulnerabilities found.
    """
    critical_vulnerabilities = []
    for result in scan_results.get("Results", []):
        for vulnerability in result.get("Vulnerabilities", []):
            if vulnerability.get("Severity") == "CRITICAL":
                critical_vulnerabilities.append(vulnerability)

    critical_count = len(critical_vulnerabilities)
    CRITICAL_VULN_GAUGE.labels(image=image_name).set(critical_count)
    print(f"Updated Prometheus metric for {image_name}: {critical_count} critical vulnerabilities.")

    return critical_vulnerabilities

if __name__ == "__main__":
    args = parse_arguments()

    # Start Prometheus HTTP server to expose metrics on port 8000
    start_http_server(9090)
    print("Prometheus metrics available at http://localhost:8000")

    while True:
        # Step 1: Scan the Docker image
        scan_results = scan_docker_image(args.podname)

        # Step 2: Save the scan results
        save_scan_results(scan_results, args.output)

        # Step 3: Analyze vulnerabilities and update Prometheus metrics
        critical_vulnerabilities = analyze_scan_results(scan_results, args.podname)

        if critical_vulnerabilities:
            print(f"Critical vulnerabilities found: {len(critical_vulnerabilities)}")
            sys.exit(1)
        else:
            print("No critical vulnerabilities found.")
            time.sleep(300)  # Sleep for 5 minutes before the next scan
