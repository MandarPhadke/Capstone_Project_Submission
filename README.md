# Docker Image Vulnerability Scanner with Historical Tracking

This project provides an automated solution to **scan Docker container images for vulnerabilities** using **Trivy**, store the scan results, and visualize historical vulnerability trends using **Prometheus and Grafana**.

## **Table of Contents**
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Prometheus Configuration](#prometheus-configuration)
- [Grafana Dashboard Setup](#grafana-dashboard-setup)
- [Usage](#usage)
- [Automation with Jenkins](#automation-with-jenkins)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## **Overview**

With the increasing adoption of containerized applications, securing container images is crucial to prevent vulnerabilities from reaching production. This project enables DevOps teams to automate container security scanning in CI/CD pipelines, store scan history, and visualize vulnerability trends.

---

## **Features**

- Automated vulnerability scanning using **Trivy**.
- Stores vulnerability data in **Prometheus** for historical tracking.
- Real-time alerts for critical vulnerabilities.
- **Grafana dashboards** for visualizing vulnerability trends.
- Integrates with CI/CD pipelines (Jenkins, GitHub Actions).
- Slack notifications for critical vulnerabilities.

---

## **Architecture**

The following diagram outlines the overall system architecture:

                    +---------------------+
                    |   Docker Container  |
                    +---------------------+
                              |
                              v
                       +-------------+
                       |    Trivy    |  (Scans images)
                       +-------------+
                              |
                              v
                  +------------------------+
                  |     Prometheus          |  (Stores vulnerability data)
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |         Grafana         |  (Visualize trends)
                  +------------------------+


---

## **Technologies Used**

- **Trivy** - Vulnerability scanner for container images.
- **Python** - Automation scripting.
- **Prometheus** - Monitoring and storing scan results.
- **Grafana** - Visualization of vulnerability history.
- **Docker** - Containerization of the scanning process.
- **Jenkins** - CI/CD automation.

---

## **Setup Instructions**

### **Prerequisites**

Ensure you have the following installed:

- Docker and Docker Compose
- Python 3.x
- Prometheus and Grafana
- Jenkins (optional)
# Container Image Vulnerability Scanner with Reporting

## Overview
This repository provides a Python-based solution for scanning Docker images for vulnerabilities using **Trivy** and sending notifications via **Slack** if critical vulnerabilities are detected. The project also includes functionality to generate PDF reports summarizing the scan results.

---

## Features
- **Trivy Integration**: Scans Docker images for vulnerabilities using Trivy.
- **Slack Notifications**: Sends notifications to a Slack channel for critical vulnerabilities.
- **PDF Reporting**: Generates detailed PDF reports for each scan.
- **Containerized Solution**: Includes a Dockerfile for running the scanner in a containerized environment.
- **CI/CD Friendly**: Easily integrates into CI/CD pipelines.

---

## Prerequisites
### For Local Setup:
1. Python 3.9 or higher.
2. Docker installed and running.
3. Trivy installed and accessible in the system path ([Installation Guide](https://aquasecurity.github.io/trivy/v0.35.0/installation/)).
4. Slack Webhook URL for sending notifications. [Create Webhook](https://api.slack.com/messaging/webhooks).

### For Docker Setup:
- Docker installed and running on your machine.

---

## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/MandarPhadke/Container-Image-Vulnerability-Scanner-with-Reporting.git
cd Container-Image-Vulnerability-Scanner-with-Reporting
```

### 2. Install Dependencies (Local Setup)
Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage
### 1. Run the Script Locally
Use the following command to scan a Docker image:
```bash
python scan_docker_pods.py --podname <docker_image_name>
```
**Example:**
```bash
python scan_docker_pods.py --podname nginx:latest
```

### 2. Run in Docker
Build the Docker image:
```bash
docker build -t vulnerability-scanner .
```
Run the container:
```bash
docker run --rm vulnerability-scanner --podname <docker_image_name>
```
**Example:**
```bash
docker run --rm vulnerability-scanner --podname nginx:latest
```

---

## Configuration
### Environment Variables
- `SLACK_WEBHOOK_URL`: Set this environment variable to your Slack Webhook URL to enable notifications.

### Example:
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/your/webhook/url"
```

---

## Output
1. **Slack Notification**:
   - Notifications for critical vulnerabilities are sent to the configured Slack channel.
2. **PDF Report**:
   - A PDF report summarizing the scan is generated in the current working directory.

---

## Project Structure
```
.
├── Dockerfile                # Dockerfile to containerize the application
├── requirements.txt          # Python dependencies
├── scan_docker_pods.py       # Main Python script to scan Docker images
├── README.md                 # Documentation
```

---

## Example Workflow
1. **Scan Docker Image**:
   - Use the `scan_docker_pods.py` script to scan an image (e.g., `nginx:latest`).
2. **Check Slack Notifications**:
   - Review notifications for any critical vulnerabilities detected.
3. **Review the PDF Report**:
   - Open the generated PDF for a detailed summary of scan results.

---

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- [Trivy](https://github.com/aquasecurity/trivy) for vulnerability scanning.
- [Slack API](https://api.slack.com/) for notifications.




