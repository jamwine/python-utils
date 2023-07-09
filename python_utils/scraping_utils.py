def scrape_xpath(response, xpath):
    try:
        data = response.xpath(xpath).extract()
    except Exception as exc:
        print(f"!! Exception encountered while scraping xpath: {xpath} !!\n", exc)
    return data
