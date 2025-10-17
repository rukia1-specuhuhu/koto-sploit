"""Advanced report generator with multiple formats"""

import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any
from colorama import Fore, Style

class AdvancedReporter:
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.scan_data = {
            "session_id": self.session_id,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "targets": [],
            "vulnerabilities": [],
            "modules_executed": []
        }
    
    def add_target(self, target: str):
        if target not in self.scan_data["targets"]:
            self.scan_data["targets"].append(target)
    
    def add_vulnerability(self, vuln: Dict[str, Any]):
        vuln["discovered_at"] = datetime.now().isoformat()
        self.scan_data["vulnerabilities"].append(vuln)
    
    def add_module_execution(self, module: str, target: str, result: Dict[str, Any]):
        self.scan_data["modules_executed"].append({
            "module": module,
            "target": target,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
    
    def finalize(self):
        self.scan_data["end_time"] = datetime.now().isoformat()
    
    def generate_json_report(self, filename: str = None):
        if not filename:
            filename = f"kotosploit_report_{self.session_id}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.scan_data, f, indent=2)
            print(f"{Fore.GREEN}[+] JSON report saved: {filename}{Style.RESET_ALL}")
            return filename
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving JSON report: {e}{Style.RESET_ALL}")
            return None
    
    def generate_csv_report(self, filename: str = None):
        if not filename:
            filename = f"kotosploit_report_{self.session_id}.csv"
        
        try:
            with open(filename, 'w', newline='') as f:
                if self.scan_data["vulnerabilities"]:
                    fieldnames = ['type', 'target', 'parameter', 'payload', 'discovered_at']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for vuln in self.scan_data["vulnerabilities"]:
                        row = {
                            'type': vuln.get('type', 'Unknown'),
                            'target': vuln.get('target', 'Unknown'),
                            'parameter': vuln.get('parameter', 'N/A'),
                            'payload': vuln.get('payload', 'N/A'),
                            'discovered_at': vuln.get('discovered_at', 'Unknown')
                        }
                        writer.writerow(row)
            
            print(f"{Fore.GREEN}[+] CSV report saved: {filename}{Style.RESET_ALL}")
            return filename
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving CSV report: {e}{Style.RESET_ALL}")
            return None
    
    def generate_xml_report(self, filename: str = None):
        if not filename:
            filename = f"kotosploit_report_{self.session_id}.xml"
        
        try:
            root = ET.Element("kotosploit_scan")
            
            session = ET.SubElement(root, "session")
            ET.SubElement(session, "id").text = self.scan_data["session_id"]
            ET.SubElement(session, "start_time").text = self.scan_data["start_time"]
            ET.SubElement(session, "end_time").text = self.scan_data["end_time"] or "In Progress"
            
            targets = ET.SubElement(root, "targets")
            for target in self.scan_data["targets"]:
                ET.SubElement(targets, "target").text = target
            
            vulnerabilities = ET.SubElement(root, "vulnerabilities")
            for vuln in self.scan_data["vulnerabilities"]:
                vuln_elem = ET.SubElement(vulnerabilities, "vulnerability")
                ET.SubElement(vuln_elem, "type").text = vuln.get('type', 'Unknown')
                ET.SubElement(vuln_elem, "target").text = vuln.get('target', 'Unknown')
                ET.SubElement(vuln_elem, "parameter").text = vuln.get('parameter', 'N/A')
                ET.SubElement(vuln_elem, "payload").text = vuln.get('payload', 'N/A')
                ET.SubElement(vuln_elem, "discovered_at").text = vuln.get('discovered_at', 'Unknown')
            
            tree = ET.ElementTree(root)
            tree.write(filename, encoding='utf-8', xml_declaration=True)
            
            print(f"{Fore.GREEN}[+] XML report saved: {filename}{Style.RESET_ALL}")
            return filename
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving XML report: {e}{Style.RESET_ALL}")
            return None
    
    def generate_html_report(self, filename: str = None):
        if not filename:
            filename = f"kotosploit_report_{self.session_id}.html"
        
        try:
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Kotosploit Security Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .header {{ background-color: #d32f2f; color: white; padding: 20px; border-radius: 5px; }}
        .section {{ background-color: white; margin: 20px 0; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f44336; color: white; }}
        .vuln {{ background-color: #ffebee; }}
        .success {{ background-color: #e8f5e9; }}
        .cat {{ font-family: monospace; white-space: pre; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🐱 Kotosploit Security Scan Report</h1>
        <p>Session ID: {self.scan_data["session_id"]}</p>
        <p>Start Time: {self.scan_data["start_time"]}</p>
        <p>End Time: {self.scan_data["end_time"] or "In Progress"}</p>
    </div>
    
    <div class="section">
        <h2>📊 Summary</h2>
        <p><strong>Targets Scanned:</strong> {len(self.scan_data["targets"])}</p>
        <p><strong>Vulnerabilities Found:</strong> {len(self.scan_data["vulnerabilities"])}</p>
        <p><strong>Modules Executed:</strong> {len(self.scan_data["modules_executed"])}</p>
    </div>
    
    <div class="section">
        <h2>🎯 Targets</h2>
        <ul>
            {"".join([f"<li>{target}</li>" for target in self.scan_data["targets"]])}
        </ul>
    </div>
    
    <div class="section">
        <h2>🔓 Vulnerabilities</h2>
        <table>
            <tr>
                <th>Type</th>
                <th>Target</th>
                <th>Parameter</th>
                <th>Payload</th>
                <th>Discovered At</th>
            </tr>
            {"".join([f'''
            <tr class="vuln">
                <td>{vuln.get('type', 'Unknown')}</td>
                <td>{vuln.get('target', 'Unknown')}</td>
                <td>{vuln.get('parameter', 'N/A')}</td>
                <td>{vuln.get('payload', 'N/A')[:50]}...</td>
                <td>{vuln.get('discovered_at', 'Unknown')}</td>
            </tr>
            ''' for vuln in self.scan_data["vulnerabilities"]])}
        </table>
    </div>
    
    <div class="section">
        <h2>📝 Module Executions</h2>
        <table>
            <tr>
                <th>Module</th>
                <th>Target</th>
                <th>Status</th>
                <th>Timestamp</th>
            </tr>
            {"".join([f'''
            <tr>
                <td>{exec.get('module', 'Unknown')}</td>
                <td>{exec.get('target', 'Unknown')}</td>
                <td>{"✓" if exec.get('result', {}).get('success') else "✗"}</td>
                <td>{exec.get('timestamp', 'Unknown')}</td>
            </tr>
            ''' for exec in self.scan_data["modules_executed"]])}
        </table>
    </div>
    
    <div class="section">
        <p style="text-align: center; color: #666;">
            Generated by Kotosploit Framework<br>
            For authorized security testing only
        </p>
    </div>
</body>
</html>
"""
            
            with open(filename, 'w') as f:
                f.write(html_content)
            
            print(f"{Fore.GREEN}[+] HTML report saved: {filename}{Style.RESET_ALL}")
            return filename
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving HTML report: {e}{Style.RESET_ALL}")
            return None
    
    def generate_all_reports(self, base_name: str = None):
        if not base_name:
            base_name = f"kotosploit_report_{self.session_id}"
        
        self.finalize()
        
        reports = []
        reports.append(self.generate_json_report(f"{base_name}.json"))
        reports.append(self.generate_csv_report(f"{base_name}.csv"))
        reports.append(self.generate_xml_report(f"{base_name}.xml"))
        reports.append(self.generate_html_report(f"{base_name}.html"))
        
        return [r for r in reports if r is not None]
    
    def print_summary(self):
        print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Scan Summary{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Session ID: {self.scan_data['session_id']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Targets: {len(self.scan_data['targets'])}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Vulnerabilities: {len(self.scan_data['vulnerabilities'])}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Modules Executed: {len(self.scan_data['modules_executed'])}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")
