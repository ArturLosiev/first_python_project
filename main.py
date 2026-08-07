import requests
import json

def get_dog_facts()->dict:
    url = "https://catfact.ninja/fact"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)


if __name__ != "__main__":
    pass
else:
    data = get_dog_facts()
    if "fact" in data:
        fact = data["fact"]
        if fact != None:
            print(f"Random fact: {fact}")
    else:
        print("No facts")
