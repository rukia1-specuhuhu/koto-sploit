"""Report generator for pentesting results"""

import json
import csv
import xml.etree.ElementTree as ET
import os
import markdown
import weasyprint
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from colorama import Fore, Style
import base64
import io
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template

class Reporter:
    def __init__(self, output_dir: str = "./reports"):
        self.results = []
        self.session_start = datetime.now()
        self.session_end = None
        self.output_dir = output_dir
        self.metadata = {
            "title": "Kotosploit Security Report",
            "author": "Kotosploit Framework",
            "version": "1.0",
            "description": "Automated security testing report"
        }
        self.targets = []
        self.vulnerabilities = []
        self.notes = []
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def add_result(self, module_name: str, result: Dict[str, Any], target: str = None):
        result_entry = {
            "timestamp": datetime.now().isoformat(),
            "module": module_name,
            "target": target,
            "result": result
        }
        self.results.append(result_entry)
        
        if result.get("vulnerabilities"):
            for vuln in result["vulnerabilities"]:
                vuln_entry = {
                    "module": module_name,
                    "target": target,
                    "timestamp": datetime.now().isoformat(),
                    **vuln
                }
                self.vulnerabilities.append(vuln_entry)
    
    def add_target(self, target: str, metadata: Dict[str, Any] = None):
        if target not in [t["target"] for t in self.targets]:
            self.targets.append({
                "target": target,
                "added_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            })
    
    def add_note(self, note: str, timestamp: Optional[str] = None):
        self.notes.append({
            "note": note,
            "timestamp": timestamp or datetime.now().isoformat()
        })
    
    def set_metadata(self, key: str, value: Any):
        self.metadata[key] = value
    
    def finalize(self):
        self.session_end = datetime.now()
    
    def generate_json_report(self, filename: str = None) -> Optional[str]:
        if not filename:
            filename = f"kotosploit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        report = {
            "metadata": self.metadata,
            "session_start": self.session_start.isoformat(),
            "session_end": self.session_end.isoformat() if self.session_end else None,
            "targets": self.targets,
            "results": self.results,
            "vulnerabilities": self.vulnerabilities,
            "notes": self.notes,
            "summary": self._generate_summary()
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"{Fore.GREEN}[+] JSON report saved to: {filepath}{Style.RESET_ALL}")
            return filepath
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving JSON report: {e}{Style.RESET_ALL}")
            return None
    
    def generate_csv_report(self, filename: str = None) -> Optional[str]:
        if not filename:
            filename = f"kotosploit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', newline='') as f:
                if self.vulnerabilities:
                    fieldnames = ['timestamp', 'module', 'target', 'type', 'severity', 'description', 'parameter', 'payload', 'evidence']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for vuln in self.vulnerabilities:
                        row = {
                            'timestamp': vuln.get('timestamp', ''),
                            'module': vuln.get('module', ''),
                            'target': vuln.get('target', ''),
                            'type': vuln.get('type', ''),
                            'severity': vuln.get('severity', ''),
                            'description': vuln.get('description', ''),
                            'parameter': vuln.get('parameter', ''),
                            'payload': vuln.get('payload', ''),
                            'evidence': vuln.get('evidence', '')
                        }
                        writer.writerow(row)
            
            print(f"{Fore.GREEN}[+] CSV report saved to: {filepath}{Style.RESET_ALL}")
            return filepath
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving CSV report: {e}{Style.RESET_ALL}")
            return None
    
    def generate_xml_report(self, filename: str = None) -> Optional[str]:
        if not filename:
            filename = f"kotosploit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            root = ET.Element("kotosploit_report")
            
            metadata = ET.SubElement(root, "metadata")
            for key, value in self.metadata.items():
                meta = ET.SubElement(metadata, key)
                meta.text = str(value)
            
            session = ET.SubElement(root, "session")
            ET.SubElement(session, "start_time").text = self.session_start.isoformat()
            ET.SubElement(session, "end_time").text = self.session_end.isoformat() if self.session_end else ""
            
            targets = ET.SubElement(root, "targets")
            for target in self.targets:
                target_elem = ET.SubElement(targets, "target")
                ET.SubElement(target_elem, "url").text = target["target"]
                ET.SubElement(target_elem, "added_at").text = target["added_at"]
                
                if target["metadata"]:
                    metadata_elem = ET.SubElement(target_elem, "metadata")
                    for key, value in target["metadata"].items():
                        meta = ET.SubElement(metadata_elem, key)
                        meta.text = str(value)
            
            results = ET.SubElement(root, "results")
            for result in self.results:
                result_elem = ET.SubElement(results, "result")
                ET.SubElement(result_elem, "timestamp").text = result["timestamp"]
                ET.SubElement(result_elem, "module").text = result["module"]
                if result["target"]:
                    ET.SubElement(result_elem, "target").text = result["target"]
                
                result_data = ET.SubElement(result_elem, "data")
                for key, value in result["result"].items():
                    data = ET.SubElement(result_data, key)
                    data.text = str(value)
            
            vulnerabilities = ET.SubElement(root, "vulnerabilities")
            for vuln in self.vulnerabilities:
                vuln_elem = ET.SubElement(vulnerabilities, "vulnerability")
                ET.SubElement(vuln_elem, "timestamp").text = vuln.get("timestamp", "")
                ET.SubElement(vuln_elem, "module").text = vuln.get("module", "")
                ET.SubElement(vuln_elem, "target").text = vuln.get("target", "")
                ET.SubElement(vuln_elem, "type").text = vuln.get("type", "")
                ET.SubElement(vuln_elem, "severity").text = vuln.get("severity", "")
                ET.SubElement(vuln_elem, "description").text = vuln.get("description", "")
                ET.SubElement(vuln_elem, "parameter").text = vuln.get("parameter", "")
                ET.SubElement(vuln_elem, "payload").text = vuln.get("payload", "")
                ET.SubElement(vuln_elem, "evidence").text = vuln.get("evidence", "")
            
            notes = ET.SubElement(root, "notes")
            for note in self.notes:
                note_elem = ET.SubElement(notes, "note")
                ET.SubElement(note_elem, "timestamp").text = note["timestamp"]
                ET.SubElement(note_elem, "content").text = note["note"]
            
            tree = ET.ElementTree(root)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            
            print(f"{Fore.GREEN}[+] XML report saved to: {filepath}{Style.RESET_ALL}")
            return filepath
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving XML report: {e}{Style.RESET_ALL}")
            return None
    
    def generate_html_report(self, filename: str = None, template_path: str = None) -> Optional[str]:
        if not filename:
            filename = f"kotosploit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        
        if template_path and os.path.exists(template_path):
            try:
                with open(template_path, 'r') as f:
                    template_content = f.read()
            except Exception as e:
                print(f"{Fore.RED}[!] Error loading template: {e}{Style.RESET_ALL}")
                return None
        else:
            template_content = self._get_default_html_template()
        
        try:
            template = Template(template_content)
            
            severity_colors = {
                "Critical": "#d32f2f",
                "High": "#f44336",
                "Medium": "#ff9800",
                "Low": "#4caf50",
                "Info": "#2196f3"
            }
            
            html_content = template.render(
                metadata=self.metadata,
                session_start=self.session_start.strftime("%Y-%m-%d %H:%M:%S"),
                session_end=self.session_end.strftime("%Y-%m-%d %H:%M:%S") if self.session_end else "In Progress",
                targets=self.targets,
                results=self.results,
                vulnerabilities=self.vulnerabilities,
                notes=self.notes,
                summary=self._generate_summary(),
                severity_colors=severity_colors
            )
            
            with open(filepath, 'w') as f:
                f.write(html_content)
            
            print(f"{Fore.GREEN}[+] HTML report saved to: {filepath}{Style.RESET_ALL}")
            return filepath
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving HTML report: {e}{Style.RESET_ALL}")
            return None
    
    def generate_markdown_report(self, filename: str = None) -> Optional[str]:
        if not filename:
            filename = f"kotosploit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            md_content = f"""# {self.metadata.get("title", "Kotosploit Security Report")}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Author:** {self.metadata.get("author", "Kotosploit Framework")}  
**Version:** {self.metadata.get("version", "1.0")}

## Executive Summary

{self._generate_summary().get("executive_summary", "")}

## Session Information

- **Start Time:** {self.session_start.strftime("%Y-%m-%d %H:%M:%S")}
- **End Time:** {self.session_end.strftime("%Y-%m-%d %H:%M:%S") if self.session_end else "In Progress"}
- **Duration:** {self.session_end - self.session_start if self.session_end else "In Progress"}
- **Targets Scanned:** {len(self.targets)}
- **Modules Executed:** {len(self.results)}
- **Vulnerabilities Found:** {len(self.vulnerabilities)}

## Targets

"""
            
            for target in self.targets:
                md_content += f"- **{target['target']}** (Added: {target['added_at']})\n"
            
            md_content += "\n## Vulnerabilities\n\n"
            
            if self.vulnerabilities:
                severity_order = ["Critical", "High", "Medium", "Low", "Info"]
                sorted_vulns = sorted(self.vulnerabilities, key=lambda x: severity_order.index(x.get("severity", "Info")) if x.get("severity") in severity_order else 4)
                
                for vuln in sorted_vulns:
                    md_content += f"### {vuln.get('type', 'Unknown')} - {vuln.get('severity', 'Unknown')}\n\n"
                    md_content += f"**Target:** {vuln.get('target', 'Unknown')}\n\n"
                    md_content += f"**Module:** {vuln.get('module', 'Unknown')}\n\n"
                    md_content += f"**Description:** {vuln.get('description', 'No description')}\n\n"
                    
                    if vuln.get('parameter'):
                        md_content += f"**Parameter:** {vuln.get('parameter')}\n\n"
                    
                    if vuln.get('payload'):
                        md_content += f"**Payload:** ```\n{vuln.get('payload')}\n```\n\n"
                    
                    if vuln.get('evidence'):
                        md_content += f"**Evidence:** ```\n{vuln.get('evidence')}\n```\n\n"
                    
                    md_content += f"**Discovered:** {vuln.get('timestamp', 'Unknown')}\n\n"
                    md_content += "---\n\n"
            else:
                md_content += "No vulnerabilities found.\n"
            
            md_content += "\n## Module Results\n\n"
            
            for result in self.results:
                md_content += f"### {result['module']}\n\n"
                md_content += f"**Timestamp:** {result['timestamp']}\n\n"
                
                if result.get('target'):
                    md_content += f"**Target:** {result['target']}\n\n"
                
                result_data = result.get('result', {})
                if isinstance(result_data, dict):
                    for key, value in result_data.items():
                        if key != "vulnerabilities":
                            md_content += f"**{key}:** {value}\n\n"
                else:
                    md_content += f"```\n{result_data}\n```\n\n"
            
            if self.notes:
                md_content += "\n## Notes\n\n"
                for note in self.notes:
                    md_content += f"- **{note['timestamp']}**: {note['note']}\n"
            
            with open(filepath, 'w') as f:
                f.write(md_content)
            
            print(f"{Fore.GREEN}[+] Markdown report saved to: {filepath}{Style.RESET_ALL}")
            return filepath
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving Markdown report: {e}{Style.RESET_ALL}")
            return None
    
    def generate_pdf_report(self, filename: str = None, html_template_path: str = None) -> Optional[str]:
        if not filename:
            filename = f"kotosploit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            html_path = self.generate_html_report(filename.replace('.pdf', '.html'), html_template_path)
            
            if not html_path:
                return None
            
            weasyprint.HTML(filename=html_path).write_pdf(filepath)
            
            print(f"{Fore.GREEN}[+] PDF report saved to: {filepath}{Style.RESET_ALL}")
            return filepath
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving PDF report: {e}{Style.RESET_ALL}")
            return None
    
    def generate_all_reports(self, base_filename: str = None) -> List[str]:
        if not base_filename:
            base_filename = f"kotosploit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.finalize()
        
        report_files = []
        
        json_file = self.generate_json_report(f"{base_filename}.json")
        if json_file:
            report_files.append(json_file)
        
        csv_file = self.generate_csv_report(f"{base_filename}.csv")
        if csv_file:
            report_files.append(csv_file)
        
        xml_file = self.generate_xml_report(f"{base_filename}.xml")
        if xml_file:
            report_files.append(xml_file)
        
        html_file = self.generate_html_report(f"{base_filename}.html")
        if html_file:
            report_files.append(html_file)
        
        md_file = self.generate_markdown_report(f"{base_filename}.md")
        if md_file:
            report_files.append(md_file)
        
        pdf_file = self.generate_pdf_report(f"{base_filename}.pdf")
        if pdf_file:
            report_files.append(pdf_file)
        
        zip_file = self._create_report_archive(report_files, f"{base_filename}.zip")
        
        return report_files + ([zip_file] if zip_file else [])
    
    def _create_report_archive(self, file_paths: List[str], archive_name: str) -> Optional[str]:
        if not file_paths:
            return None
        
        archive_path = os.path.join(self.output_dir, archive_name)
        
        try:
            with zipfile.ZipFile(archive_path, 'w') as zipf:
                for file_path in file_paths:
                    zipf.write(file_path, os.path.basename(file_path))
            
            print(f"{Fore.GREEN}[+] Report archive created: {archive_path}{Style.RESET_ALL}")
            return archive_path
        except Exception as e:
            print(f"{Fore.RED}[!] Error creating report archive: {e}{Style.RESET_ALL}")
            return None
    
    def send_report_email(self, to_email: str, subject: str, smtp_server: str, smtp_port: int, 
                          username: str, password: str, report_files: List[str] = None) -> bool:
        if not report_files:
            base_filename = f"kotosploit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            report_files = [
                self.generate_html_report(f"{base_filename}.html"),
                self.generate_pdf_report(f"{base_filename}.pdf")
            ]
            report_files = [f for f in report_files if f]
        
        if not report_files:
            print(f"{Fore.RED}[!] No report files to send{Style.RESET_ALL}")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(f"""
            <p>Dear recipient,</p>
            <p>Please find attached the security report generated by Kotosploit Framework.</p>
            <p>Report details:</p>
            <ul>
                <li>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</li>
                <li>Targets: {len(self.targets)}</li>
                <li>Vulnerabilities: {len(self.vulnerabilities)}</li>
            </ul>
            <p>Best regards,<br>Kotosploit Framework</p>
            """, "html"))
            
            for file_path in report_files:
                with open(file_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
                    msg.attach(part)
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
            
            print(f"{Fore.GREEN}[+] Report sent to {to_email}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[!] Error sending report email: {e}{Style.RESET_ALL}")
            return False
    
    def _generate_summary(self) -> Dict[str, Any]:
        severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Info": 0}
        
        for vuln in self.vulnerabilities:
            severity = vuln.get("severity", "Info")
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        executive_summary = ""
        
        if severity_counts["Critical"] > 0:
            executive_summary = f"Critical security vulnerabilities detected ({severity_counts['Critical']} critical issues). Immediate remediation required."
        elif severity_counts["High"] > 0:
            executive_summary = f"High-severity security vulnerabilities detected ({severity_counts['High']} high issues). Prompt remediation recommended."
        elif severity_counts["Medium"] > 0:
            executive_summary = f"Medium-severity security issues detected ({severity_counts['Medium']} medium issues). Remediation advised."
        elif severity_counts["Low"] > 0:
            executive_summary = f"Low-severity security issues detected ({severity_counts['Low']} low issues). Remediation suggested when possible."
        else:
            executive_summary = "No significant security vulnerabilities detected. System appears to be secure."
        
        return {
            "executive_summary": executive_summary,
            "severity_counts": severity_counts,
            "total_vulnerabilities": sum(severity_counts.values()),
            "total_targets": len(self.targets),
            "total_modules": len(self.results),
            "session_duration": str(self.session_end - self.session_start) if self.session_end else "In Progress"
        }
    
    def _get_default_html_template(self) -> str:
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ metadata.title }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .header p {
            margin: 10px 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }
        .card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .card h2 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .summary-item {
            background: white;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .summary-item h3 {
            margin: 0 0 10px;
            color: #2c3e50;
        }
        .summary-item .value {
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e1e1e1;
        }
        th {
            background-color: #f8f9fa;
            font-weight: 600;
        }
        tr:hover {
            background-color: #f8f9fa;
        }
        .severity {
            padding: 4px 8px;
            border-radius: 4px;
            color: white;
            font-weight: bold;
            font-size: 0.8em;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #7f8c8d;
            font-size: 0.9em;
        }
        pre {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: monospace;
        }
        .badge {
            display: inline-block;
            padding: 3px 7px;
            font-size: 0.8em;
            font-weight: bold;
            border-radius: 10px;
            background-color: #e9ecef;
            color: #495057;
            margin-right: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ metadata.title }}</h1>
        <p>Generated by {{ metadata.author }} on {{ session_start }}</p>
    </div>
    
    <div class="card">
        <h2>Executive Summary</h2>
        <p>{{ summary.executive_summary }}</p>
    </div>
    
    <div class="summary-grid">
        <div class="summary-item">
            <h3>Targets</h3>
            <div class="value">{{ summary.total_targets }}</div>
        </div>
        <div class="summary-item">
            <h3>Modules</h3>
            <div class="value">{{ summary.total_modules }}</div>
        </div>
        <div class="summary-item">
            <h3>Vulnerabilities</h3>
            <div class="value">{{ summary.total_vulnerabilities }}</div>
        </div>
        <div class="summary-item">
            <h3>Critical</h3>
            <div class="value" style="color: #d32f2f;">{{ summary.severity_counts.Critical }}</div>
        </div>
        <div class="summary-item">
            <h3>High</h3>
            <div class="value" style="color: #f44336;">{{ summary.severity_counts.High }}</div>
        </div>
        <div class="summary-item">
            <h3>Medium</h3>
            <div class="value" style="color: #ff9800;">{{ summary.severity_counts.Medium }}</div>
        </div>
    </div>
    
    <div class="card">
        <h2>Session Information</h2>
        <p><strong>Start Time:</strong> {{ session_start }}</p>
        <p><strong>End Time:</strong> {{ session_end }}</p>
        <p><strong>Duration:</strong> {{ summary.session_duration }}</p>
    </div>
    
    <div class="card">
        <h2>Targets</h2>
        <ul>
            {% for target in targets %}
            <li><strong>{{ target.target }}</strong> <span class="badge">{{ target.added_at }}</span></li>
            {% endfor %}
        </ul>
    </div>
    
    <div class="card">
        <h2>Vulnerabilities</h2>
        {% if vulnerabilities %}
        <table>
            <thead>
                <tr>
                    <th>Type</th>
                    <th>Severity</th>
                    <th>Target</th>
                    <th>Module</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                {% for vuln in vulnerabilities %}
                <tr>
                    <td>{{ vuln.type }}</td>
                    <td><span class="severity" style="background-color: {{ severity_colors[vuln.severity] }};">{{ vuln.severity }}</span></td>
                    <td>{{ vuln.target }}</td>
                    <td>{{ vuln.module }}</td>
                    <td>{{ vuln.description }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <p>No vulnerabilities found.</p>
        {% endif %}
    </div>
    
    <div class="card">
        <h2>Module Results</h2>
        {% for result in results %}
        <h3>{{ result.module }}{% if result.target %} - {{ result.target }}{% endif %}</h3>
        <p><strong>Timestamp:</strong> {{ result.timestamp }}</p>
        {% if result.result.vulnerabilities %}
        <p><strong>Vulnerabilities Found:</strong> {{ result.result.vulnerabilities|length }}</p>
        {% endif %}
        {% if result.result.success %}
        <p><strong>Status:</strong> <span style="color: green;">Success</span></p>
        {% else %}
        <p><strong>Status:</strong> <span style="color: red;">Failed</span></p>
        {% endif %}
        {% if result.result.message %}
        <p><strong>Message:</strong> {{ result.result.message }}</p>
        {% endif %}
        {% if result.result.output %}
        <pre>{{ result.result.output }}</pre>
        {% endif %}
        {% endfor %}
    </div>
    
    {% if notes %}
    <div class="card">
        <h2>Notes</h2>
        <ul>
            {% for note in notes %}
            <li><strong>{{ note.timestamp }}:</strong> {{ note.note }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}
    
    <div class="footer">
        <p>Generated by {{ metadata.author }} | Version {{ metadata.version }}</p>
        <p>This report was generated automatically by the Kotosploit Framework.</p>
    </div>
</body>
</html>
        """
    
    def show_summary(self):
        summary = self._generate_summary()
        
        print(f"\n{Fore.YELLOW}Session Summary{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"  Start: {self.session_start}")
        print(f"  End: {self.session_end if self.session_end else 'In Progress'}")
        print(f"  Duration: {summary['session_duration']}")
        print(f"  Targets: {summary['total_targets']}")
        print(f"  Modules executed: {summary['total_modules']}")
        print(f"  Total vulnerabilities: {summary['total_vulnerabilities']}")
        print(f"  Critical: {summary['severity_counts']['Critical']}")
        print(f"  High: {summary['severity_counts']['High']}")
        print(f"  Medium: {summary['severity_counts']['Medium']}")
        print(f"  Low: {summary['severity_counts']['Low']}")
        print(f"  Info: {summary['severity_counts']['Info']}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}Executive Summary:{Style.RESET_ALL} {summary['executive_summary']}\n")
