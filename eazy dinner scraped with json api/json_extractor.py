import requests
import json
import time

def scrape_eazydiner_master(max_pages=1, filename="final_restaurant_data.json"):
    session = requests.Session()
    all_final_data = []
    # Note: If this BUILD_ID fails, you must refresh it from the browser URL
    BUILD_ID = "ezOfOEYvK0vDLMPQaEMCY"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.eazydiner.com/"
    }

    for p in range(1, max_pages + 1):
        print(f"\n--- 📄 PROCESSING PAGE {p} ---")
        list_url = f"https://www.eazydiner.com/_next/data/{BUILD_ID}/en/restaurants.json?location=delhi-ncr&page={p}"
        
        try:
            resp = session.get(list_url, headers=headers, timeout=10)
            # The listing path remains the same as your earlier successful analysis
            listing_data = resp.json().get("pageProps", {}).get("listingData", {}).get("data", {}).get("data", [])

            if not listing_data:
                print("🏁 No more listing data found.")
                break

            for item in listing_data:
                res_slug = item.get("res_code") 
                if not res_slug: continue

                city = res_slug.split('/')[0]
                slug_id = res_slug.split('/')[-1]

                detail_url = f"https://www.eazydiner.com/_next/data/{BUILD_ID}/en/{res_slug}.json?deal_types[]=postpaid&city={city}&restaurants_details={slug_id}"
                
                try:
                    print(f"🔍 Deep Scraping: {slug_id}")
                    detail_resp = session.get(detail_url, headers=headers, timeout=10)
                    full_json = detail_resp.json()
                    
                    # Path confirmed: pageProps -> detailPage -> data
                    page_props = full_json.get("pageProps", {})
                    res_info = page_props.get("detailPage", {}).get("data", {})

                    if not res_info:
                        print(f"⚠️ Data missing in detailPage for {slug_id}")
                        continue

                    # 1. Address & Geo Logic
                    loc = res_info.get("location", {})
                    
                    # 2. Timing Logic
                    raw_timings = res_info.get("timings", {}).get("week", {})
                    
                    # 3. FAQ Logic (Limit to 4)
                    faq_array = []
                    for faq in res_info.get("faq", [])[:4]: # Slicing the list to first 4
                        faq_array.append({
                            "question": faq.get("name"),
                            "answer": faq.get("acceptedAnswer", {}).get("text") if isinstance(faq.get("acceptedAnswer"), dict) else ""
                        })

                    # --- ADDED FEATURES SECTION ---
                    features_list = [f.get("name") for f in res_info.get("webEngageData", {}).get("features", [])]

                    all_final_data.append({
                        "name": res_info.get("name"),
                        "category": res_info.get("category"),
                        "avg_rating": res_info.get("user_reviews", {}).get("avg_rating"),
                        "price_range": res_info.get("priceRange") or res_info.get("cost_for_two"),
                        "telephone": res_info.get("phone") or res_info.get("telephone"),
                        "timings": format_timings(raw_timings),
                        "features": features_list, # Included in data
                        "address": {
                            "street": loc.get("address"),
                            "locality": loc.get("locality"),
                            "region": loc.get("region_code") or "",
                        },
                        "geo": {
                            "lat": loc.get("latitude"),
                            "lng": loc.get("longitude")
                        },
                        "faqs": faq_array,
                    })

                    time.sleep(1.2) 

                except Exception as e:
                    print(f"⚠️ Detail Error: {e}")

        except Exception as e:
            print(f"❌ List Error: {e}")

    # Final Save
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_final_data, f, indent=4, ensure_ascii=False)
    print(f"\n✨ SUCCESS! {len(all_final_data)} Master Records saved to {filename}")

def format_timings(week_dict):
    if not week_dict: return "Not Available"
    try:
        times = [t[0] if isinstance(t, list) else t for t in week_dict.values() if t]
        if times and len(set(times)) == 1:
            return f"Mon-Sun: {times[0]}"
    except: pass
    return str(week_dict)

# Start the engine
scrape_eazydiner_master(max_pages=20)