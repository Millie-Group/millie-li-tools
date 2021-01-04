from SearchScraper import SearchScraper
from selenium.webdriver import Chrome
from utils import HEADLESS_OPTIONS
import json
from ProfileScraper import ProfileScraper
from scrape import scrape_profile


def handler(event, context):
    args = json.loads(event["body"])

    # sets up a Selenium instance using Chrome
    driver_options = HEADLESS_OPTIONS
    driver_type = Chrome

    # initializes a scraper object based on the cookie to scrape the URL's profile
    searcher = SearchScraper(driver=driver_type, email=args["email"], password=args["password"],
                             driver_options=driver_options)
    results = searcher.scrape(url=args["url"])

    if args["scrapeAll"] == "T":
        profiles = {}
        for result in results:
            scraper = ProfileScraper(driver=driver_type, email=args["email"], password=args["password"],
                                     driver_options=driver_options)
            fullName, firstName, lastName, location, locs, undergrad, all_schools, \
            yrs_experience, headline, int_hs, undergrad_yr = scrape_profile(scraper, result['url'])

            profile = {"fullName": fullName,
                                "firstName": firstName,
                                "lastName": lastName,
                                "location": location,
                                "otherLocs": locs,
                                "undergrad": undergrad,
                                "otherSchools": all_schools,
                                "yrsExp": yrs_experience,
                                "headline": headline,
                                "intHS": int_hs,
                                "undergradYr": undergrad_yr}
            profiles[result['url']] = profile

        return {"statusCode": 200,
                "body": json.dumps(profiles)}
    else:
        print(json.dumps(results))
        return {"statusCode": 200,
                "body": json.dumps(results)}