import webbse
import get_ip
import asyncio
import toml
import traceback

import sys

async def run(cfg_file_path: str):
    cfg = toml.load(cfg_file_path)

    username = cfg["username"]
    api_key = open(cfg["api_key_location"], "r").read().strip()
    domain, wait_time = cfg["domain"], cfg["wait"]

    webb_se_api = webbse.WebbSE(username, api_key)

    last_ip = None
    while True:
        try:
            ip = await get_ip.get_ip()
            if ip == last_ip:
                continue
            print(f"IP changed from {last_ip} to {ip}. Updating.")
            await webb_se_api.update_a_record(domain, ip)
            last_ip = ip
        except Exception as e:
            traceback.print_exc()
        finally:
            await asyncio.sleep(wait_time)

asyncio.run(run(sys.argv[1]))
