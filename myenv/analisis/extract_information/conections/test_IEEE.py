from playwright.sync_api import sync_playwright, Page, expect
import pandas as pd
import sys
import os
import time
import glob

#agregue esto para que me reconociera los modulos, pq de resto no quiso
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


from analisis.extract_information.conections.credentials import username, password
#este es el metodo unificar
from analisis.results_information.unification import unificar


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

def createLinkExtractInformation(pageNumber, textToFind: str):
    textFormat = textToFind.replace(" ","%20")
    link_extractInformation = f"https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?newsearch=true&queryText={textFormat}&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&rowsPerPage=100&pageNumber={pageNumber}"
    return link_extractInformation

def extract_information(page: Page, text: str):
    login(page, username, password)

    # Wait until the URL is the expected one
    while not page.url.startswith(link_IEEE):
        page.wait_for_timeout(1000)  # Wait 1 second before checking again
    
    # Verify that the URL is the expected one after login
    expect(page).to_have_url(link_IEEE)
    
    results = []
    for i in range(1, 3):  # Asegúrate de que el rango sea correcto
        try:
            # Navigate to the desired URL
            page.goto(createLinkExtractInformation(i, text))
            # Extract all list results items
            page.wait_for_selector('div.col.result-item-align.px-3')
            items = page.query_selector_all('div.col.result-item-align.px-3')

            for item in items:
                title = item.query_selector('h3 a').inner_text()
                link = item.query_selector('h3 a').get_attribute('href')
                
                # Check if the author element exists
                author_element = item.query_selector('p.author')
                authors = author_element.inner_text() if author_element else 'N/A'
                
                conference = item.query_selector('div.description a').inner_text()
                year = item.query_selector('span[xplhighlight]').inner_text()
                results.append({'Title': title, 'Link': link, 'Authors': authors, 'Conference': conference, 'Year': year})
        except Exception as e:
            print(f"Error on page {i}: {e}")
            page.wait_for_timeout(5000)  # Espera 5 segundos antes de intentar la siguiente página

    # Save results to CSV (this will overwrite the file if it already exists)
    df = pd.DataFrame(results)
    df.to_csv('results.csv', index=False)
    print("Results saved to results.csv")

def test(page: Page):
    extract_information(page, input("Ingresa el texto que deseas buscar:\n"))

# Run the test
with sync_playwright() as p:
    # Specify the download directory
    browser = p.chromium.launch(headless=False, downloads_path='analisis/extract_information/archivos_csv_IEEE')
    page = browser.new_page()
    test(page)
    browser.close()

    #la idea era que cuando descarguen los 3 haga la union y tire los biptext
    # cantidad_archivos=3

    # tiempo_inicio = time.time()
    # while time.time() - tiempo_inicio < 60:
    #     #archivos = [f for f in os.listdir("analisis/extract_information/conections") if f.endswith(".csv")]
    #     archivos = glob.glob("analisispy/myenv/analisis/extract_information/conections/*.csv")
    #     if len(archivos) >= cantidad_archivos:  
    #         print(f"✅ {len(archivos)} archivos descargados: {archivos}")
    #         unificar()
    # time.sleep(6)  # Revisa cada 6 segundos
    # print(f"⚠️ No se descargaron al menos {cantidad_archivos} archivos en {60} segundos.{len(archivos)}")



