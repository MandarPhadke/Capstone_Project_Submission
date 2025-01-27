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

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/yourusername/Container-Image-Vulnerability-Scanner-with-Reporting.git
cd Container-Image-Vulnerability-Scanner-with-Reporting


