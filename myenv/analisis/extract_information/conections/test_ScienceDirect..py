import re
from playwright.sync_api import sync_playwright, Page, expect
import pandas as pd

# Define the URLs
link = "https://login.intelproxy.com/v2/conector/google/solicitar?cuenta=7Ah6RNpGWF22jjyq&url=ezp.2aHR0cHM6Ly9pZWVleHBsb3JlLmllZWUub3JnL3NlYXJjaC9zZWFyY2hyZXN1bHQuanNwP2FjdGlvbj1zZWFyY2gmbmV3c2VhcmNoPXRydWU-"
link_IEEE = "https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?action=search&newsearch=true"

def login(page: Page, username: str, password: str):
    # Navigate to the desired URL
    page.goto(link)

    # Fill in the email input field with the username
    page.fill('input[type="email"]', username)

    # Click the "Next" button
    page.click("#identifierNext")

    # Wait for the password input field to be visible
    page.wait_for_selector('input[type="password"]')

    # Fill in the password input field with the password
    page.fill('input[type="password"]', password)

    # Click the "Next" button after entering the password
    page.click("#passwordNext")

def createLinkExtractInformation(pageNumber):
    link_extractInformation = f"https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?action=search&newsearch=true&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&rowsPerPage=100&pageNumber="+str(pageNumber)
    return link_extractInformation

def extract_information(page: Page):
    login(page, "juand.guzmang@uqvirtual.edu.co", "Juandajedrez20251")
    
    # Wait until the URL is the expected one
    while not page.url.startswith(link_IEEE):
        page.wait_for_timeout(1000)  # Wait 1 second before checking again
    
    # Verify that the URL is the expected one after login
    expect(page).to_have_url(link_IEEE)
    
    results = []
    for i in range(1, 11):  # Asegúrate de que el rango sea correcto
        # Navigate to the desired URL
        page.goto(createLinkExtractInformation(i))
        # Extract all list results items
        page.wait_for_selector('div.col.result-item-align.px-3')
        items = page.query_selector_all('div.col.result-item-align.px-3')

        for item in items:
            title = item.query_selector('h3 a').inner_text()
            link = item.query_selector('h3 a').get_attribute('href')
            authors = item.query_selector('p.author').inner_text()
            conference = item.query_selector('div.description a').inner_text()
            year = item.query_selector('span[xplhighlight]').inner_text()
            results.append({'Title': title, 'Link': link, 'Authors': authors, 'Conference': conference, 'Year': year})

    # Save results to CSV (this will overwrite the file if it already exists)
    df = pd.DataFrame(results)
    df.to_csv('results.csv', index=False)
    print("Results saved to results.csv")

def test(page: Page):
    extract_information(page)

# Run the test
with sync_playwright() as p:
    # Specify the download directory
    browser = p.chromium.launch(headless=False, downloads_path='analisis/extract_information/archivos_csv_IEEE')
    page = browser.new_page()
    test(page)
    browser.close()