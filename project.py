import requests
import subprocess
import socket
from urllib import parse
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin



def clickjacking(domain):
    print("*************************Clickjacking vulnarbility*************************")
    headers = requests.get(domain).headers
    if 'X-Frame-Options' in headers:
        print ("Not Vulnarable to clickjacking")
    else:
        print ("Vulnarable By Clickjacking vulnarbility")



"""*************************XSS vulnarbility*************************"""

def get_all_forms(domain):
    """Given a `url`, it returns all forms from the HTML content"""
    soup = bs(requests.get(domain).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """
    This function extracts all possible useful information about an HTML `form`
    """
    details = {}
    # get the form action (target url)
    action = form.attrs.get("action", "").lower()
    # get the form method (POST, GET, etc.)
    method = form.attrs.get("method", "get").lower()
    # get all the input details such as type and name
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def submit_form(form_details, domain, value):
    # construct the full URL (if the url provided in action is relative)
    target_url = urljoin(domain, form_details["action"])
    # get the inputs
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        # replace all text and search values with `value`
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            # if input name and value are not None, 
            # then add them to the data of form submission
            data[input_name] = input_value

    print(f"[+] Submitting malicious payload to {target_url}")
    print(f"[+] Data: {data}")
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        # GET request
        return requests.get(target_url, params=data)

def scan_xss(domain):
    print("*************************XSS vulnarbility*************************")
    # get all the forms from the URL
    forms = get_all_forms(domain)
    print(f"[+] Detected {len(forms)} forms on {domain}.")
    js_script = "<Script>alert('hi')</scripT>"
    # returning value
    is_vulnerable = False
    # iterate over all forms
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, domain, js_script).content.decode()
        if js_script in content:
            print(f"[+] XSS Detected on {domain}")
            print(f"[*] Form details:")
            pprint(form_details)
            is_vulnerable = True
    return is_vulnerable



"""*************************SQL injection vulnarbility*************************"""

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
def is_vulnerable(response, payload, url):
    """A function that checks if a response indicates SQL Injection vulnerability."""
    errors = {
        # MySQL
        "you have an error in your sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",
    }
    for error in errors:
        if error in response.content.decode().lower():
            print("[+] SQL Injection vulnerability detected in URL:", url)
            print("[+] Payload:", payload)
            return True
    return False


def check_rce(url):
    print("*************************RCE vulnarbility*************************")
    # get all the forms from the URL
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    # returning value
    is_vulnerable = False
    # iterate over all forms
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, "test; echo vulnerable").content.decode()
        if "vulnerable" in content:
            print(f"[+] RCE vulnerability detected, link:", url)
            print(f"[*] Form details:")
            pprint(form_details)
            is_vulnerable = True
    return is_vulnerable

# def check_csrf(url):
#     print("*************************CSRF vulnarbility*************************")
#     # get the CSRF token
#     res = s.get(url)
#     soup = bs(res.content, "html.parser")
#     csrf = soup.find("input", attrs={"name": "csrf_token"})["value"]
#     print("[+] CSRF token obtained:", csrf)
#     # craft the data
#     data = {
#         "csrf_token": csrf,
#         "username": "admin",
#         "password": "admin",
#     }
#     # make the login request
#     res = s.post(url, data=data)
#     return "logged in" in res.content.decode()



def scan_sql_injection(url):
    print("*************************SQL INJECTION vulnarbility*************************")

    # test on URL
    for c in "\"'":
        # add quote/double quote character to the URL
        new_url = f"{url}{c}"
        print("[!] Trying", new_url)
        # make the HTTP request
        res = s.get(new_url)
        if is_vulnerable(res,c, new_url):
            return
    # test on HTML forms
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    file = open('payloads.txt', 'r')
    payloads = file.read().splitlines()

    for form in forms:
        form_details = get_form_details(form)
        for payload in payloads:
            # the data body we want to submit
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag.get("type") == "hidden" or input_tag.get("value"):
                    # any input form that is hidden or has some value,
                    # just use it in the form body
                    try:
                        data[input_tag["name"]] = input_tag.get("value","") + payload
                    except KeyError:
                        pass
                elif input_tag["type"] != "submit":
                    # all others except submit, use some junk data with special character
                    data[input_tag["name"]] = f"test{payload}"
            # join the url with the action (form request URL)
            url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = s.post(url, data=data)
            elif form_details["method"] == "get":
                res = s.get(url, params=data)
            # test whether the resulting page is vulnerable
            if is_vulnerable(res, payload, url):
                print("[+] SQL Injection vulnerability detected, link:", url)
                break


def check_lfi(url):
        print("*************************LFI vulnarbility*************************")
        lfi_payloads = ["../../../../../../../../../../../etc/passwd",
                         "../../../../../../../../../../../etc/passwd",
                         "/..././..././..././..././..././..././..././etc/passwd%00",
                         "../../../../../../../..//etc/passwd"]

        for payload in lfi_payloads:
            r = requests.get(url + payload, timeout=5)
            if "root:x" in r.text:
                print("[+]" +"LFI vulnerability found at %s%s" % (url, payload))
            else:
                print("[-]" +"LFI is not found at %s%s" % (url, payload))
        return False




"""*************************main function*************************"""       

if __name__ == "__main__":
    domain = input("Enter the domain : ")
    clickjacking(domain)
    check_lfi(domain)
    scan_sql_injection(domain)
    check_rce(domain)
    check_csrf(domain)
    print(scan_xss(domain))
    


