import requests

url = "https://www.valueresearchonline.com/funds/10603/sbi-small-cap-fund/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)

with open("page.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("Saved page.html")