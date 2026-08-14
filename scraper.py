import httpx


class Scraper:
    GET_URL = "https://catfact.ninja/fact"
    POST_URL = "http://127.0.0.1:8000/add-fact"

    @staticmethod
    def get_fact() -> dict | None:
        response = httpx.get(Scraper.GET_URL, timeout=5.0)
        response.raise_for_status()
        data = response.json()
        fact = data.get("fact")
        if fact is None:
            return None
        return {"fact": fact}

    @staticmethod
    def post_fact(payload: dict | str, author: str = "Anonymous") -> dict:
        if isinstance(payload, str):
            body = {"new_fact": payload, "author": author}
        else:
            body = {
                "new_fact": payload["fact"],
                "author": payload.get("author", author),
            }

        response = httpx.post(Scraper.POST_URL, json=body, timeout=5.0)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    fact = Scraper.get_fact()
    if fact is None:
        print("No fact received")
    else:
        result = Scraper.post_fact(fact)
        print(result)
