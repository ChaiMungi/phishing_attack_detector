# importing required packages for this module
import pandas as pd
import numpy as np
from urllib.parse import urlparse,urlencode
import ipaddress
import re


# Loading legitimate files
data1 = pd.read_csv("1.Benign_list_big_final.csv")
data1.columns = ['URLs']
print(data1.head())

# Collecting 5,000 Legitimate URLs randomly
legiurl = data1.sample(n=5000, random_state=12).copy()
legiurl = legiurl.reset_index(drop=True)
print(legiurl.head())

print(legiurl.shape)




# importing required packages for this section
from urllib.parse import urlparse,urlencode
import ipaddress
import re


# 1.Domain of the URL (Domain)
def getDomain(url):
    domain = urlparse(url).netloc
    if re.match(r"^www.", domain):
        domain = domain.replace("www.", "")
    return domain


# 2.Checks for IP address in URL (Have_IP)
def havingIP(url):
    try:
        ipaddress.ip_address(url)
        ip = 1
    except:
        ip = 0
    return ip


# 3.Checks the presence of @ in URL (Have_At)
def haveAtSign(url):
    if "@" in url:
        at = 1
    else:
        at = 0
    return at


# 4.Finding the length of URL and categorizing (URL_Length)
def getLength(url):
    if len(url) < 54:
        length = 0
    else:
        length = 1
    return length


# 5.Gives number of '/' in URL (URL_Depth)
def getDepth(url):
    s = urlparse(url).path.split('/')
    depth = 0
    for j in range(len(s)):
        if len(s[j]) != 0:
            depth = depth + 1
    return depth


# 6.Checking for redirection '//' in the url (Redirection)
def redirection(url):
    pos = url.rfind('//')
    if pos > 6:
        if pos > 7:
            return 1
        else:
            return 0
    else:
        return 0


# 7.Existence of “HTTPS” Token in the Domain Part of the URL (https_Domain)
def httpDomain(url):
    domain = urlparse(url).netloc
    if 'https' in domain:
        return 1
    else:
        return 0


# listing shortening services
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"


# 8. Checking for Shortening Services in URL (Tiny_URL)
def tinyURL(url):
    match = re.search(shortening_services, url)
    if match:
        return 1
    else:
        return 0


# 9.Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1
    else:
        return 0


import re
from bs4 import BeautifulSoup
import whois
import urllib
import urllib.request
from datetime import datetime


# 11.DNS Record availability (DNS_Record)
# obtained in the featureExtraction function itself

# 12.Web traffic (Web_Traffic)
def web_traffic(url):
    try:
        # Filling the whitespaces in the URL if any
        url = urllib.parse.quote(url)
        rank = \
        BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(),"xml").find("REACH")['RANK']
        rank = int(rank)
    except TypeError:
        return 1
    if rank < 100000:
        return 1
    else:
        return 0


# 13.Survival time of domain: The difference between termination time and creation time (Domain_Age)
def domainAge(domain_name):
    creation_date = domain_name.creation_date
    expiration_date = domain_name.expiration_date
    if (isinstance(creation_date, str) or isinstance(expiration_date, str)):
        try:
            creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            return 1
    if ((expiration_date is None) or (creation_date is None)):
        return 1
    elif ((type(expiration_date) is list) or (type(creation_date) is list)):
        return 1
    else:
        ageofdomain = abs((expiration_date - creation_date).days)
        if ((ageofdomain / 30) < 6):
            age = 1
        else:
            age = 0
    return age


# 14.End time of domain: The difference between termination time and current time (Domain_End)
def domainEnd(domain_name):
    expiration_date = domain_name.expiration_date
    if isinstance(expiration_date, str):
        try:
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            return 1
    if (expiration_date is None):
        return 1
    elif (type(expiration_date) is list):
        return 1
    else:
        today = datetime.now()
        end = abs((expiration_date - today).days)
        if ((end / 30) < 6):
            end = 0
        else:
            end = 1
    return end


# importing required packages for this section
import requests


# 15. IFrame Redirection (iFrame)
def iframe(response):
    if response == "":
        return 1
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            return 0
        else:
            return 1


# 16.Checks the effect of mouse over on status bar (Mouse_Over)
def mouseOver(response):
    if response == "":
        return 1
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            return 1
        else:
            return 0


# 17.Checks the status of the right click attribute (Right_Click)
def rightClick(response):
    if response == "":
        return 1
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            return 0
        else:
            return 1


# 18.Checks the number of forwardings (Web_Forwards)
def forwarding(response):
    if response == "":
        return 1
    else:
        if len(response.history) <= 2:
            return 0
        else:
            return 1

def get_dns_record(url):
    dns = 0
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except:
        dns = 1
    return dns


def get_Domain_age(url):
    dns = 0
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except:
        dns = 1
    if dns == 1:
        return 1
    else:
        domainAge(domain_name)

def get_Domain_end(url):
    dns = 0
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except:
        dns = 1
    if dns == 1:
        return 1
    else:
        domainEnd(domain_name)

def get_iframe(url):
    try:
        response = requests.get(url)
    except:
        response = ""
    return iframe(response)

def get_Mouse_Over(url):
    try:
        response = requests.get(url)
    except:
        response = ""
    return mouseOver(response)

def get_Right_Click_response(url):
    try:
        response = requests.get(url)
    except:
        response = ""
    return rightClick(response)

def get_Web_Forwards(url):
    try:
        response = requests.get(url)
    except:
        response = ""
    return forwarding(response)

# Function to extract features
def featureExtraction(url, label):
    print("\n In the featureExtraction")
    features = []
    # Address bar based features (10)
    features.append(getDomain(url))
    features.append(havingIP(url))
    features.append(haveAtSign(url))
    features.append(getLength(url))
    features.append(getDepth(url))
    features.append(redirection(url))
    features.append(httpDomain(url))
    features.append(tinyURL(url))
    features.append(prefixSuffix(url))
    print("\n In the featureExtraction after address based features")
    # Domain based features (4)
    dns = 0
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except:
        dns = 1

    features.append(dns)
    features.append(web_traffic(url))
    features.append(1 if dns == 1 else domainAge(domain_name))
    features.append(1 if dns == 1 else domainEnd(domain_name))


    # HTML & Javascript based features (4)
    try:
        response = requests.get(url)
    except:
        response = ""
    features.append(iframe(response))
    features.append(mouseOver(response))
    features.append(rightClick(response))
    features.append(forwarding(response))
    features.append(label)

    return features




data0 = pd.read_csv("2.online-valid.csv")
print(data0.head())

phishurl = data0.sample(n = 5000, random_state = 12).copy()
phishurl = phishurl.reset_index(drop=True)
df_grp = phishurl.groupby(["url"])[["Label"]].sum().reset_index()
print("\n PRINTING URL AND LABEL")
print(df_grp.head())
df_grp["Domain"] = df_grp.url.apply(getDomain)
df_grp["havingIP"] = df_grp.url.apply(havingIP)
df_grp["haveAtSign"] = df_grp.url.apply(haveAtSign)
df_grp["getLength"] = df_grp.url.apply(getLength)
df_grp["redirection"] = df_grp.url.apply(redirection)
df_grp["httpDomain"] = df_grp.url.apply(httpDomain)
df_grp["tinyURL"] = df_grp.url.apply(tinyURL)
df_grp["prefixSuffix"] = df_grp.url.apply(prefixSuffix)
#df_grp["web_traffic"] = df_grp.url.apply(web_traffic)
df_grp["DNS_record"] = df_grp.url.apply(get_dns_record)
df_grp["Domain_Age"] = df_grp.url.apply(get_Domain_age)
df_grp["Domain_End"] = df_grp.url.apply(get_Domain_end)
df_grp["iFrame"] = df_grp.url.apply(get_iframe)
df_grp["Mouse_Over"] = df_grp.url.apply(get_Mouse_Over)
df_grp["Right_Click"] = df_grp.url.apply(get_Right_Click_response)
df_grp["Web_Forwards"] = df_grp.url.apply(get_Web_Forwards)
print("\n PRINTING DATA GROUP")
print(df_grp)
df_grp.to_csv("5.url_info.csv")


# Storing the data in CSV file
#urldata.to_csv('urldata.csv', index=False)

def extract_features_of_inp_url(url):
    print("\n In the extract_features_of_inp_url")
    label = 1
    phish_features = featureExtraction(url, label)
    print(phish_features)
    feature_names = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection','https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record', 'Web_Traffic','Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over', 'Right_Click', 'Web_Forwards', 'Label']
    print(len(phish_features))
    print(len(feature_names))
    print(type(phish_features))
    print(type(feature_names))
    phishing = pd.DataFrame(data=[phish_features],columns=['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection','https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record', 'Web_Traffic','Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over', 'Right_Click', 'Web_Forwards', 'Label'])
    print(type(phishing))
    phishing.drop(columns=['Domain','Label'],inplace=True)
    #phishing.to_csv('legitimate.csv', index= False)
    return phishing