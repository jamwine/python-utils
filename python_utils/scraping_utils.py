def scrape_xpath(response, xpath):
    """
    Scrapes data from a web response using the provided XPath expression.

    Parameters:
        response (object): The web response object.
        xpath (str): The XPath expression to extract data from the response.

    Returns:
        list: The scraped data as a list of strings, or None if no data is found.

    Raises:
        ValueError: If the xpath parameters is invalid.

    Example:
        response = ...
        xpath = '//div[@class="content"]//p/text()'
        scraped_data = scrape_xpath(response, xpath)
    """
    # Validate the xpath parameter
    if not xpath or not isinstance(xpath, str):
        raise ValueError("Invalid xpath.")

    try:
        data = response.xpath(xpath).extract()
    except Exception as exc:
        print(f"!! Exception encountered while scraping xpath: {xpath} !!\n", exc)
        return None

    return data if data else None


def get_full_urls(root_url, urls):
    """
    Generates full URLs by concatenating a root URL with a list of relative URLs.

    Parameters:
        root_url (str): The root URL to prepend to the relative URLs.
        urls (list): A list of relative URLs.

    Returns:
        list: A list of full URLs.

    Raises:
        ValueError: If the root_url parameter is not a string or the urls parameter is not a list.

    Example:
        root_url = 'https://example.com/'
        urls = ['page1.html', 'page2.html', 'page3.html']
        full_urls = get_full_urls(root_url, urls)
    """
    # Validate root_url parameter
    if not isinstance(root_url, str):
        raise ValueError("The root_url parameter must be a string.")

    # Validate urls parameter
    if not isinstance(urls, list):
        raise ValueError("The urls parameter must be a list.")

    # Ensure root_url ends with a forward slash
    if not root_url.endswith('/'):
        root_url += '/'

    # Generate full URLs by concatenating root_url and relative URLs
    return [root_url + url.strip('/') for url in urls if url.strip('/')]


def extract_urls_from_xpath(response, xpath, root_url):
    """
    Extracts URLs from a web response using the provided XPath expression and generates full URLs.

    Parameters:
        response (object): The web response object.
        xpath (str): The XPath expression to extract URLs from the response.
        root_url (str): The root URL to prepend to the extracted relative URLs.

    Returns:
        set: A set of full URLs.

    Raises:
        ValueError: If the xpath parameter is invalid.

    Example:
        response = ...
        xpath = '//a/@href'
        root_url = 'https://example.com/'
        urls = extract_urls_from_xpath(response, xpath, root_url)
    """
    urls = scrape_xpath(response, xpath)
    return set(get_full_urls(root_url, urls)) if urls else None
