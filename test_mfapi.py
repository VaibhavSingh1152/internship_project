import requests

scheme_code = "120503"  # SBI Bluechip Fund example

url = f"https://api.mfapi.in/mf/{scheme_code}"

data = requests.get(url).json()

print("Scheme:", data["meta"]["scheme_name"])
print("Records:", len(data["data"]))

print("\nLatest 5 NAV entries:")
for d in data["data"][:5]:
    print(d)