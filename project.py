import requests
import argparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests
import json
from jinja2 import Template  # For HTML report
from reportlab.lib.pagesizes  import letter
from reportlab.pdfgen import canvas
import sqlite3
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from pprint import pprint
import time
import textwrap

vulnerabilities = []  # List to store all vulnerabilities found


def generate_timestamp():
    return time.strftime("%Y%m%d%H%M%S")

# Function to create a SQLite database and tables
def create_database():
    conn = sqlite3.connect('vulnerability_scanner.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scanned_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            clickjacking_status TEXT,
            lfi_status TEXT,
            sql_injection_status TEXT,
            rce_status TEXT,
            csrf_status TEXT,
            xss_status TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert scan results into the database
def insert_scan_results(url, clickjacking_status, lfi_status, sql_injection_status, rce_status, csrf_status, xss_status):
    conn = sqlite3.connect('vulnerability_scanner.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO scanned_urls (
            url, clickjacking_status, lfi_status, sql_injection_status, rce_status, csrf_status, xss_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (url, clickjacking_status, lfi_status, sql_injection_status, rce_status, csrf_status, xss_status))
    conn.commit()
    conn.close()


    
def clickjacking_scan(domain):
    print("*************************Clickjacking vulnerability*************************")
    headers = requests.get(domain).headers
    if 'X-Frame-Options' in headers:
        print("Not Vulnerable to clickjacking")
    else:
        print("Vulnerable to Clickjacking vulnerability")
        vulnerabilities.append({
            "url": domain,
            "type": "Clickjacking",
            "severity": "High",  # Adjust severity as needed
            "details": "This website is vulnerable to Clickjacking. It allows embedding in iframes.",
            "mitigation": "Implementing the X-Frame-Options header with the value SAMEORIGIN or DENY in your web application's response will mitigate Clickjacking. SAMEORIGIN only allows the page to be loaded in an iframe if the request originates from the same domain, and DENY denies all attempts to load the page in an iframe."
            
        })

def get_all_forms(url):
    """Given a `url`, it returns all forms from the HTML content"""
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    """Extracts useful information about an HTML `form`"""
    details = {}
    details["action"] = form.attrs.get("action", "").lower()
    details["method"] = form.attrs.get("method", "get").lower()
    details["inputs"] = [{"type": input_tag.attrs.get("type", "text"),
                          "name": input_tag.attrs.get("name")} for input_tag in form.find_all("input")]
    return details

def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    data = {input["name"]: value for input in form_details["inputs"]}
    print(f"[+] Submitting payload to {target_url}")
    print(f"[+] Data: {data}")
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

def xss_scan(url):
    print("*************************XSS vulnerability*************************")
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    js_script = "<Script>alert('hi')</script>"
    is_vulnerable = False
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            print(f"[+] XSS Detected on {url}")
            print(f"[*] Form details:")
            pprint(form_details)
            is_vulnerable = True
    if is_vulnerable:
        vulnerabilities.append({
            "url": url,
            "type": "XSS",
            "severity": "Medium",  # Adjust severity as needed
            "details": "This website is vulnerable to Cross-Site Scripting (XSS). The scan detected malicious JavaScript injection.",
            "mitigation": "To mitigate XSS, input validation and output encoding should be implemented. Ensure that user-generated content is properly sanitized and not executed as JavaScript in the browser. Also, use security headers such as Content Security Policy (CSP) to restrict script sources."
        })
    return is_vulnerable

def is_sql_injection_vulnerable(response, payload, url):
    """Check if a response indicates SQL Injection vulnerability."""
    errors = {"you have an error in your sql syntax;",
              "warning: mysql",
              "unclosed quotation mark after the character string",
              "quoted string not properly terminated"}
    for error in errors:
        if error in response.content.decode().lower():
            print("[+] SQL Injection vulnerability detected in URL:", url)
            print("[+] Payload:", payload)
            return True
    return False

def sql_injection_scan(url):
    print("*************************SQL Injection vulnerability*************************")
    # vulnerabilities_found = []
    for c in "\"'":
        new_url = f"{url}{c}"
        print("[!] Trying", new_url)
        res = requests.get(new_url)
        if is_sql_injection_vulnerable(res, c, new_url):
            # vulnerabilities_found.append(c)
            vulnerabilities.append({
            "url": url,
            "type": "SQL Injection",
            "severity": "High",  # Adjust severity as needed
            "details": "This website is vulnerable to SQL Injection. The scan detected potential SQL Injection points.",
            "mitigation": "To mitigate SQL Injection, use parameterized queries or prepared statements in your database interactions. Avoid constructing SQL queries with user-provided data without proper validation and sanitization."
            })
        continue
    # if vulnerabilities_found:
        

def rce_scan(url):
    print("*************************RCE vulnerability*************************")
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    is_vulnerable = False
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, "test; echo vulnerable").content.decode()
        if "vulnerable" in content:
            print(f"[+] RCE vulnerability detected, link:", url)
            print(f"[*] Form details:")
            pprint(form_details)
            is_vulnerable = True
            vulnerabilities.append({
                "url": url,
                "type": "RCE",
                "severity": "High",  # Adjust severity as needed
                "details": "This website is vulnerable to Remote Code Execution (RCE). The scan detected a potential RCE payload in the response.",
                "mitigation": "To mitigate RCE vulnerabilities, implement strict input validation, and avoid executing untrusted data as commands or scripts on the server. Review and sanitize user inputs, and restrict external command execution."
            })
        
    return is_vulnerable

def csrf_scan(url):
    print("*************************CSRF vulnerability*************************")
    # Get the CSRF token if it exists
    res = requests.get(url)
    soup = bs(res.content, "html.parser")
    csrf_element = soup.find("input", attrs={"name": "csrf_token"})
    if csrf_element:
        csrf = csrf_element.get("value", "")
        print("[+] CSRF token obtained:", csrf)
        vulnerabilities.append({
            "url": url,
            "type": "CSRF",
            "severity": "Low",  # Adjust severity as needed
            "details": "This website is vulnerable to Cross-Site Request Forgery (CSRF). The scan detected the presence of a CSRF token, which could be exploited by attackers.",
            "mitigation": "To mitigate CSRF vulnerabilities, implement anti-CSRF tokens in your web application. Use unique tokens for each session and ensure that the application verifies the token with each request to prevent unauthorized actions."
        })
    else:
        print("[-] CSRF token not found on the page")


def lfi_scan(url):
    print("*************************LFI vulnerability*************************")
    lfi_payloads = ["../../../../../../../../../../../etc/passwd",
                    "../../../../../../../../../../../etc/passwd",
                    "/..././..././..././..././..././..././..././etc/passwd%00",
                    "../../../../../../../../../../../etc/passwd"]
    for payload in lfi_payloads:
        r = requests.get(url + payload, timeout=5)
        if "root:x" in r.text:
            print("[+]" + "LFI vulnerability found at %s%s" % (url, payload))
            vulnerabilities.append({
                "url": url,
                "type": "LFI",
                "severity": "Low",  # Adjust severity as needed
                "details": "This website is vulnerable to Local File Inclusion (LFI). The scan detected access to sensitive system files.",
                "mitigation": "To mitigate LFI, validate and sanitize user input, and avoid including files from untrusted sources. Implement proper file path restrictions and access controls."
            })
        else:
            print("[-]" + "LFI is not found at %s%s" % (url, payload))
    return False

def perform_scan(url, scan_clickjacking, scan_lfi, scan_sql_injection, scan_rce, scan_csrf, scan_xss):
    create_database()  # Create the database if not exists

    if scan_clickjacking:
        clickjacking_status = clickjacking_scan(url)
    else:
        clickjacking_status = "Not Scanned"

    if scan_lfi:
        lfi_status = lfi_scan(url)
    else:
        lfi_status = "Not Scanned"

    if scan_sql_injection:
        sql_injection_status = sql_injection_scan(url)
    else:
        sql_injection_status = "Not Scanned"

    if scan_rce:
        rce_status = rce_scan(url)
    else:
        rce_status = "Not Scanned"

    if scan_csrf:
        csrf_status = csrf_scan(url)
    else:
        csrf_status = "Not Scanned"

    if scan_xss:
        xss_status = xss_scan(url)
    else:
        xss_status = "Not Scanned"

    # Insert scan results into the database
    insert_scan_results(url, clickjacking_status, lfi_status, sql_injection_status, rce_status, csrf_status, xss_status)


def new_draw(c, y_position, difference):
    if y_position - difference < 20:
        c.showPage()
        y_position = letter[1] - 20
        return c, y_position
    else:
        return c, y_position 

def generate_report(vulnerabilities):
    timestamp = generate_timestamp()
    html_report_filename = f'report.html'
    json_report_filename = f'report.json'
    pdf_report_filename = f'report.pdf' 
    # Generate an HTML report
    with open(html_report_filename, 'w') as f:
        template = Template('report_template.html')  # Use your HTML template
        rendered_report = template.render(vulnerabilities=vulnerabilities)
        f.write(rendered_report)
    # Generate a JSON report
    with open(json_report_filename, 'w') as f:
        json.dump(vulnerabilities, f, indent=4)

    # Generate a PDF report
    # c = canvas.Canvas(pdf_report_filename, pagesize=letter)
    # c.drawString(100, 750, 'Vulnerability Report')  # Customize as needed
    # y_position = 700
    # for vulnerability in vulnerabilities:
    #     y_position -= 20
    #     c.drawString(100, y_position, f"URL: {vulnerability['url']}")
    #     c.drawString(100, y_position - 20, f"Type: {vulnerability['type']}")
    #     c.drawString(100, y_position - 40, f"Severity: {vulnerability['severity']}")
    #     c.drawString(100, y_position - 60, f"Details: {vulnerability['details']}")
    #     c.drawString(100, y_position - 80, f"Mitigation: {vulnerability['mitigation']}")
    # c.save()
    c = canvas.Canvas(pdf_report_filename, pagesize=letter)
    c.drawString(250, letter[1] - 20, 'Vulnerability Report',)  # Customize as needed
    y_position = letter[1] - 30
    mitigation_displayed = False  # Flag to track whether Mitigation title has been displayed
    z = 0
    for vulnerability in vulnerabilities:
        y_position -= 100
        z += 1
        c.drawString(100, y_position + 70, f"Vulnerability inx: [{z}]")
        c, y_position = new_draw(c, y_position, 100)
        c.drawString(100, y_position + 50 , f"URL: {vulnerability['url']}")
        c, y_position = new_draw(c, y_position, 50)
        c.drawString(100, y_position + 30, f"Type: {vulnerability['type']}")
        c, y_position = new_draw(c, y_position, 30)
        c.drawString(100, y_position + 10, f"Severity: {vulnerability['severity']}")
        c, y_position = new_draw(c, y_position, 10)
        wrapped_details = textwrap.wrap(vulnerability['details'], width=70)
        i = 0
        for line in wrapped_details:
            if i == 0:
                line = "Details: " + line
            c.drawString(100, y_position - 20, line)
            c, y_position = new_draw(c, y_position, 20)
            y_position -= 20
            i += 1
        y_position -= 10
        wrapped_mitigation = textwrap.wrap(vulnerability['mitigation'], width=70)
        i = 0
        for line in wrapped_mitigation:
            if i == 0:
                line = "Mitigation: " + line
            c.drawString(100, y_position - 20, line)
            c, y_position = new_draw(c, y_position, 20)
            y_position -= 20
            i += 1
        y_position -= 10
        c, y_position = new_draw(c, y_position, 10)
        c.drawString(100, y_position - 20, "------------------------------------------------------------------------------------------------------------------")
        y_position -= 20
        c, y_position = new_draw(c, y_position, 20)
        
        # add a page if there is more content
 
        
            

    c.save()





# CLI setup
def setup_cli():
    parser = argparse.ArgumentParser(description="Web Application Vulnerability Scanner")
    parser.add_argument("url", help="Target URL for scanning")
    parser.add_argument("--clickjacking", action="store_true", help="Scan for Clickjacking vulnerabilities")
    parser.add_argument("--lfi", action="store_true", help="Scan for Local File Inclusion (LFI) vulnerabilities")
    parser.add_argument("--sql-injection", action="store_true", help="Scan for SQL Injection vulnerabilities")
    parser.add_argument("--rce", action="store_true", help="Scan for Remote Code Execution (RCE) vulnerabilities")
    parser.add_argument("--csrf", action="store_true", help="Scan for Cross-Site Request Forgery (CSRF) vulnerabilities")
    parser.add_argument("--xss", action="store_true", help="Scan for Cross-Site Scripting (XSS) vulnerabilities")
    parser.add_argument("--all", action="store_true", help="Scan for all vulnerabilities")
    return parser.parse_args()

# Main function
def main():
    args = setup_cli()

    if args.all:
        perform_scan(args.url, True, True, True, True, True, True)
    else:
        perform_scan(args.url, args.clickjacking, args.lfi, args.sql_injection, args.rce, args.csrf, args.xss)

    # Generate a report
    generate_report(vulnerabilities)
    

if __name__ == "__main__":
    main()
