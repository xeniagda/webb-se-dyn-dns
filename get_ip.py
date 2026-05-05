import aiohttp

async def get_ip() -> str:
    async with aiohttp.ClientSession() as s:
        r = await s.get("https://api.ipify.org/")
        return await r.text()

if __name__ == "__main__":
    import time
    import asyncio

    async def main():
        last_ip = None
        last_ip_at = time.time()

        while True:
            start = time.time()
            ip = await get_ip()
            if ip == last_ip:
                continue

            took = time.time() - start
            print(f"My ip is {ip}, found in {took*1e3:.1f} ms", end="")
            if last_ip != None:
                time_since = start - last_ip_at
                print(f" (change after {time_since / 60 / 60:.1f} h)")
            else:
                print()
            last_ip = ip
            last_ip_at = start

    asyncio.run(main())
