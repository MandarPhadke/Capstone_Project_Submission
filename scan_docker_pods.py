import subprocess
import os, sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import simpleSplit
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


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


def send_email(smtp_server: str, smtp_port: int, sender_email: str, sender_password: str, recipient_email: str, pod_name: str, scan_results: dict, attachment_path: str):
    """
    Send the Trivy scan results via Gmail with an attachment.

    Args:
        smtp_server (str): SMTP server address (e.g., smtp.gmail.com).
        smtp_port (int): SMTP server port (e.g., 587).
        sender_email (str): Sender's Gmail address.
        sender_password (str): Sender's Gmail password.
        recipient_email (str): Recipient's email address.
        pod_name (str): The name of the Docker pod.
        scan_results (dict): Trivy scan results in JSON format.
        attachment_path (str): Path to the file to attach.
    """
    try:
        print("Preparing email...")

        # Create the email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = f"Trivy Scan Results for Docker Pod: {pod_name}"

        # Build the email body
        vulnerabilities = scan_results.get("Results", [])
        message_body = f"Scan results for Docker pod: {pod_name}\n\n"
        if not vulnerabilities:
            message_body += "No vulnerabilities found!"
            return 0
        else:
            message_body += "Vulnerabilities found. Please check the attached PDF.\n"
        message.attach(MIMEText(message_body, "plain"))

        # Attach the PDF file
        if attachment_path and os.path.exists(attachment_path):
            print(f"Attaching file: {attachment_path}")
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(attachment_path)}",
            )
            message.attach(part)
        else:
            print(f"Attachment file not found: {attachment_path}")
            return 1

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade connection to secure
            server.login(sender_email, sender_password)
            server.send_message(message)
            print("Email sent successfully.")
        return 1
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")


def generate_pdf_from_json(json_data, output_file):
    """
    Generate a PDF document with tables and colors from JSON data.

    Args:
        json_data (dict): The JSON data to display in the PDF.
        output_file (str): The path to save the PDF file.
    """
    try:
        # Initialize the PDF document
        doc = SimpleDocTemplate(output_file, pagesize=landscape(letter))
        elements = []

        # Add title
        styles = getSampleStyleSheet()
        title = Paragraph("Vulnerability Scan Report", styles["Title"])
        elements.append(title)

        # Add metadata summary table
        metadata = [
            ["Artifact Name", json_data.get("ArtifactName", "Unknown")],
            ["Artifact Type", json_data.get("ArtifactType", "Unknown")],
            ["Generated At", json_data.get("GeneratedAt", "Unknown")],
        ]
        metadata_table = Table(metadata, colWidths=[150, 350])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(metadata_table)
        elements.append(Paragraph("<br/>", styles["Normal"]))  # Add spacing

        # Add vulnerabilities table
        vulnerabilities = json_data.get("Results", [])
        for result in vulnerabilities:
            target = result.get("Target", "Unknown Target")
            elements.append(Paragraph(f"<b>Target:</b> {target}", styles["Heading2"]))

            vuln_data = result.get("Vulnerabilities", [])
            if not vuln_data:
                elements.append(Paragraph("No vulnerabilities found.", styles["Normal"]))
            else:
                # Create table for vulnerabilities
                data = [["ID", "Title", "Severity", "Fixed Version"]]
                for vuln in vuln_data:
                    data.append([
                        vuln.get("VulnerabilityID", "N/A"),
                        vuln.get("Title", "N/A"),
                        vuln.get("Severity", "N/A"),
                        vuln.get("FixedVersion", "N/A")
                    ])

                # Wrap text in cells
                col_widths = [100, 250, 100, 150]
                wrapped_data = wrap_text_in_cells(data, col_widths, styles["BodyText"])

                vuln_table = Table(wrapped_data, colWidths=col_widths)
                vuln_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(vuln_table)
                elements.append(Paragraph("<br/>", styles["Normal"]))  # Add spacing

        # Build the PDF
        doc.build(elements)
        
        print(f"PDF report successfully generated: {output_file}")

    except Exception as e:
        print(f"Error generating PDF: {e}")

def scan_image(image_name: str, output_file: str = None):
    """
    Scan a Docker image using Trivy and save the output.

    Args:
        image_name (str): The name of the Docker image to scan.
        output_file (str, optional): Path to save the scan results. Defaults to None.
    """
    try:
        print(f"Scanning image: {image_name} using Trivy...")
        # Run the Trivy command
        command = ["trivy", "image", "--format", "json", image_name]
        result = subprocess.run(command, capture_output=True, text=True)

        # Check if the scan was successful
        if result.returncode != 0:
            print("Error during scanning:")
            print(result.stderr)
            return

        # Parse the JSON output
        scan_results = json.loads(result.stdout)

        # Save to file if an output path is provided
        if output_file:
            with open(output_file, "w") as file:
                json.dump(scan_results, file, indent=4)
            print(f"Scan results saved to {output_file}")
        else:
            print(json.dumps(scan_results, indent=4))
        return scan_results

    except Exception as e:
        print(f"Error: {e}")



def wrap_text_in_cells(data, col_widths, style):
    """
    Wrap text in table cells to prevent overlapping.

    Args:
        data (list): The table data (list of lists).
        col_widths (list): List of column widths.
        style: Paragraph style for wrapping text.

    Returns:
        list: Table data with wrapped text.
    """
    wrapped_data = []
    for row in data:
        wrapped_row = []
        for col_index, cell in enumerate(row):
            if isinstance(cell, str):
                # Wrap text based on column width
                wrapped_cell = Paragraph(cell, style)
                wrapped_row.append(wrapped_cell)
            else:
                wrapped_row.append(cell)
        wrapped_data.append(wrapped_row)
    return wrapped_data


if __name__ == "__main__":
    #pod_name = "prashanth153/nodejs-backend"
    parser = argparse.ArgumentParser(description="Scan Docker Pods")
    parser.add_argument("--podname", required=True, help="Name of the pod to scan")
    args = parser.parse_args()
    pod_name = args.podname
    output = "../logs/"+pod_name+".json"
    PDF_output = "../reports/"+pod_name+".pdf"
    status = 1
    # Ensure paths are absolute
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    output = os.path.abspath(os.path.join(base_dir, output))
    PDF_output = os.path.abspath(os.path.join(base_dir, PDF_output))

    # Step 1: Scan the Docker image and save results
    if pod_name:
        scan_results = scan_image(pod_name, output)

        # Step 2: Generate the PDF report
        if os.path.exists(output):
            with open(output, "r") as json_file:
                json_data = json.load(json_file)
                generate_pdf_from_json(json_data, PDF_output)

            # Step 3: Send the email with the generated PDF
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "mandarphadke1434@gmail.com"
            sender_password = "jphh kzsx nabv sqcf"
            recipient_email = "mandarphadke1434@gmail.com"

            if os.path.exists(PDF_output):
                status = send_email(
                    smtp_server=smtp_server,
                    smtp_port=smtp_port,
                    sender_email=sender_email,
                    sender_password=sender_password,
                    recipient_email=recipient_email,
                    pod_name=pod_name,
                    scan_results=scan_results,
                    attachment_path=PDF_output,
                )
                sys.exit(status)
            else:
                print(f"PDF report not found at {PDF_output}")
                sys.exit(status)
        else:
            print(f"JSON scan results not found at {output}")
            sys.exit(status)
    else:
        print("No pod name specified. Exiting.")
        sys.exit(status)

    

    
