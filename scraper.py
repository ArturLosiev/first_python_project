import httpx
import asyncio

class Scraper:
    GET_URL = "https://catfact.ninja/fact"
    POST_URL = "http://127.0.0.1:8000/add-fact"

    @staticmethod
    async def fetch_fact() -> dict | None:
        async with httpx.AsyncClient() as client:
            response = await client.get(Scraper.GET_URL, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            fact = data.get("fact")
            if fact is None:
                return None
            return {"fact": fact}

    @staticmethod
    async def post_fact(payload: dict | str, author: str = "Anonymous") -> dict:
        async with httpx.AsyncClient() as client:
            if isinstance(payload, str):
                body = {"new_fact": payload, "author": author}
            else:
                body = {
                    "new_fact": payload["fact"],
                    "author": payload.get("author", author),
                }

            response = await client.post(Scraper.POST_URL, json=body, timeout=5.0)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def main() -> None:
        print("Fetching 10 facts...")
        fetch_tasks = [Scraper.fetch_fact() for _ in range(10)]
        results = await asyncio.gather(*fetch_tasks)

        valid_results = [r for r in results if r is not None]

        print(f"Posting {len(valid_results)} facts to the server...")
        post_tasks = [Scraper.post_fact(result) for result in valid_results]
        await asyncio.gather(*post_tasks)

        print("Finished!")


if __name__ == "__main__":
    asyncio.run(Scraper.main())
