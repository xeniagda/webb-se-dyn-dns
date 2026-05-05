import aiohttp

BASE_URL = "https://www.webb.se/api2"

class WebbSE:
    def __init__(
        self,
        username: str,
        api_key: str,
    ):
        self.username = username
        self.api_key = api_key

    def _make_session(self):
        return aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.username, self.api_key))

    async def list_domains(
        self,
        domain: str,
    ):
        async with self._make_session() as s:
            req = await s.get(f"{BASE_URL}/webbdns/{domain}")
            data = await req.json()
            return (await req.json())["data"]["dnsrecords"]

    async def update_a_record(
        self,
        domain: str,
        ip: str,
    ):
        # find ID for domain
        domain_name_top = ".".join(domain.split(".")[-2:])
        subdomains = await self.list_domains(domain_name_top)
        matching = [d for d in subdomains if d["name"] == domain + "." and d["recordtype"] == "A"]
        if len(matching) == 0:
            raise ValueError(f"Found no domain matching {domain} (there are records for {[(d['name'], d['recordtype']) for d in subdomains]})")
        if len(matching) > 1:
            raise ValueError(f"Found many domains matching {domain}: {matching!r}")

        old_record = matching[0]

        async with self._make_session() as s:
            pass
            req = await s.put(
                f"{BASE_URL}/webbdns/{domain_name_top}/update",
                data={
                    "name": domain + ".",
                    "new_content": ip,
                    "old_content": old_record["recordcontent"],
                    "type": "A",
                },
            )
            if req.status != 200:
                data = await req.data()
                raise ValueError(f"Failed: {data}")

if __name__ == "__main__":
    import asyncio

    username = "xenia.loov"
    key = open("/tmp/key", "r").read().strip()
    api = WebbSE(username, key)
    async def list_domains():
        l = await api.list_domains("60.nu")
        for row in l:
            print(row)

    asyncio.run(list_domains())
    # asyncio.run(api.update_a_record("test.60.nu", "6.9.6.9"))
