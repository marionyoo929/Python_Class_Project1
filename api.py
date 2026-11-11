import requests

URL = "https://rest-api-test-self.vercel.app/api/3"


def get_rest_api_data():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    rows = []
    for item in data:
        address = item["address"]
        geo = address["geo"]
        rows.append([
            item["id"],
            item["email"],
            item["first_name"],
            item["last_name"],
            item["avatar"],
            address["street"],
            address["city"],
            address["zipcode"],
            geo["lat"],
            geo["lng"],
        ])
    return rows
