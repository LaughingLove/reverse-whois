from bs4 import BeautifulSoup
import requests
import urllib.parse as parse

name_or_email = input("Enter registrant name or email address: ")
parsed_name = parse.quote(name_or_email)


url = "https://viewdns.info/reversewhois/?q={}".format(parsed_name)
# Faking browser header so cloudflare doesn't block us
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.get(url, headers=headers)

data = r.text
soup = BeautifulSoup(data, features="html.parser")
# Finding the specific table that has our info
table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('border') and tag['border']=="1")

if table:
    # Finding the rows in the table
    rows = table.find_all("tr")
    #Excluding the first row because it doesn't contain a domain
    for row in rows[1:]:
        tds = row.find_all("td")
        # Finding the first column of that row, which contains the domain
        domain = tds[0].contents[0]
        print(domain)
else:
    print("Person/Email not found!")
