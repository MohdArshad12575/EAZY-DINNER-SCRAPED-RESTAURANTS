# import requests
# from concurrent.futures import ThreadPoolExecutor

# # New Free API URL
# API_URL = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all&skip=0&limit=2000"

# def validate_one(proxy):
#     proxy = proxy.strip()
#     if not proxy: return None
#     proxy_url = f"http://{proxy}"
#     try:
#         # Testing against a neutral endpoint to ensure the proxy is alive
#         r = requests.get("https://httpbin.org/ip", proxies={"http": proxy_url, "https": proxy_url}, timeout=10)
#         if r.status_code == 200:
#             return proxy_url
#     except:
#         return None

# def main():
#     try:
#         # 1. Fetch
#         response = requests.get(API_URL)
#         if response.status_code != 200: return

#         raw_list = [p.strip() for p in response.text.splitlines() if p.strip()]
#         if not raw_list: return

#         print(f"--- Validating {len(raw_list)} proxies. Please wait... ---")

#         # 2. Validate (Silent)
#         with ThreadPoolExecutor(max_workers=100) as executor:
#             results = list(executor.map(validate_one, raw_list))

#         working_proxies = [res for res in results if res is not None]

#         # 3. Save
#         with open("valid_proxies.txt", "w") as f:
#             for p in working_proxies:
#                 f.write(p + "\n")
        
#         print(f"--- Done! Saved {len(working_proxies)} working proxies to valid_proxies.txt ---")

#     except Exception:
#         pass 

# if __name__ == "__main__":
#     main()