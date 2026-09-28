import requests

def search_fund(query):
    url = "https://api.mfapi.in/mf"
    data = requests.get(url).json()

    results = []

    for item in data:
        if query.lower() in item["schemeName"].lower():
            results.append({
                "name": item["schemeName"],
                "code": item["schemeCode"]
            })

    return results[:10]