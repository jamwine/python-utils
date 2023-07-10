def scrape_xpath(response, xpath):
    try:
        data = response.xpath(xpath).extract()
    except Exception as exc:
        print(f"!! Exception encountered while scraping xpath: {xpath} !!\n", exc)
    return data


def get_full_urls(root_url, urls):
    return [root_url + url for url in urls if url != '']


def extract_urls_from_xpath(response, xpath, root_url):
    data = scrape_xpath(response, xpath)
    data = set(get_full_urls(root_url, data))
    return data