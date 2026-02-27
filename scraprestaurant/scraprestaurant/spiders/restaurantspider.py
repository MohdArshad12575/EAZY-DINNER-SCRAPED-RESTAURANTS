import scrapy

class RestaurantspiderSpider(scrapy.Spider):
    name = "restaurantspider"
    allowed_domains = ["www.eazydiner.com"]
    start_urls = ["https://www.eazydiner.com/restaurants?location=delhi-ncr"]

    def parse(self, response):
        """ LEVEL 1: Main Listing Page """
        # Extract the 9 restaurant links from the current page
        restaurant_links = response.css('div.listing_res_name__uVIN8 h3 a::attr(href)').getall()

        for link in restaurant_links:
            # Follow each link to the Restaurant Home Page
            yield response.follow(link, callback=self.parse_restaurant_home)

        # PAGINATION: After looping through 9 links, find the 'Next' page link
        next_page = response.xpath("//a[contains(text(), 'Next')]/@href").get()
        if next_page:
            # Follow to the next page and repeat Level 1 logic
            yield response.follow(next_page, callback=self.parse)

    def parse_restaurant_home(self, response):
        """ LEVEL 2: Individual Restaurant Home Page """
        # Find the specific 'About' tab link
        # Using a partial match for the class to keep it future-proof
        about_link = response.xpath("//a[contains(text(), 'about')]/@href").get()

        if about_link:
            yield response.follow(about_link, callback=self.parse_about_page)

    def parse_about_page(self, response):
        """ LEVEL 3: The Final About Page (Data Extraction) """
        
        # 1. Name
        name = response.xpath("//h1/text()").get()

        # 2. Rating
        rating = response.xpath("//span[contains(@class, 'rating_text_color')]/text()").get()

        # 3. Price
        price = response.xpath("//div[contains(text(), 'for two')]/text()").get()

        # 4. Timing (Cleaning the 'Today,' prefix)
        raw_timing = response.xpath("//div[contains(@class, 'open_time')]//div/text()[contains(., 'PM')]").get()
        clean_timing = raw_timing.replace('Today, ', '').strip() if raw_timing else None

        # 5. Address
        address = response.xpath("//div[a[contains(@class, 'map_container')]]/div[contains(@class, 'grey')]/text()").get()

        # 6. Features (Extracting as a list)
        features = response.xpath("//div[contains(@class, 'restaurantDetails_features_container')]//a/text()").getall()

        #cuisines
        cuisines = response.xpath('//div[contains(@class, "restaurantDetails_cuisines_list")]/text()').getall()
        cuisine_type = ", ".join([c.strip() for c in cuisines if c.strip()])

        # YIELD THE FINAL ITEM
        yield {
            "restaurant_name": name.strip() if name else None,
            "location": address.strip() if address else None,
            "rating": rating,
            "timings": {
                "Mon-Sun": clean_timing
            },
            "restaurant_details": {
                "Cuisine Type": cuisine_type,
                "Price Band": price.strip() if price else None,
                "Live Sports Screening" : "Yes" if "Live Sports Screening" in features else "No",
                "Parking Availability" : "Yes" if "Parking" in features else "No",
                "Valet Parking" : "Yes" if "Valet Parking" in features else "No",
                "Luxury Dining" : "Yes" if "Luxury Dining" in features else "No",
                "Live Music": "Yes" if "Live Music" in features else "No",
                "DJ": "Yes" if "DJ" in features else "No",
                "Romantic Suitability" : "Yes" if "Romantic" in features else "No",
                "Take-away" : "Yes" if "Take-away" in features else "No",
                "Home Delivery" : "Yes" if "Home Delivery" in features else "No",
                "5-star dining" : "Yes" if "5-star dining" in features else "No",
                "Outdoor Seating" : "Yes" if "Outdoor Seating" in features else "No",
                "Air Condition Availability" : "Yes" if "Air Condition" in features else "No",
                "Alcohol Availability": "Yes" if "Alcohol Served" in features else "No",
            }
        }