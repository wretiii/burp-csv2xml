import xml.etree.ElementTree as ET
import csv
import argparse
import re

# Setup command line argument parsing
parser = argparse.ArgumentParser(description='Convert Burp Suite XML output to CSV.')
parser.add_argument('-i', '--input', required=True, help='Input XML file')
parser.add_argument('-o', '--output', required=True, help='Output CSV file')
args = parser.parse_args()

def clean_html_tags(text):
    return re.sub('<[^<]+?>', '', text) if text else ''

# Parse the XML file
tree = ET.parse(args.input)
root = tree.getroot()

# Open the CSV file for writing
with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Severity', 'Host', 'Path', 'Full Path', 'Issue Detail', 'Name', 'Issue Background', 'Remediation Background']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for issue in root.findall('.//issue'):
        host = clean_html_tags(issue.find('host').text if issue.find('host') is not None else '')
        path = clean_html_tags(issue.find('path').text if issue.find('path') is not None else '')
        full_path = f"{host}{path}"
        writer.writerow({
            'Severity': issue.find('severity').text,
            'Host': host,
            'Path': path,
            'Full Path': full_path,
            'Issue Detail': clean_html_tags(issue.find('issueDetail').text if issue.find('issueDetail') is not None else ''),
            'Name': clean_html_tags(issue.find('name').text if issue.find('name') is not None else ''),
            'Issue Background': clean_html_tags(issue.find('issueBackground').text if issue.find('issueBackground') is not None else ''),
            'Remediation Background': clean_html_tags(issue.find('remediationBackground').text if issue.find('remediationBackground') is not None else '')
        })
