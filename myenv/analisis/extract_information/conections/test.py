import os
import sys

import pandas as pd
from analisis.extract_information.conections.credentials import (password,
                                                                 username)
from playwright.sync_api import Page, expect, sync_playwright

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from analisis.extract_information.conections.credentials import (password,
                                                                 username)
from analisis.results_information.unification import unification

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


def createLinkExtractInformation_IEEE(pageNumber, textToFind: str):
    textFormat = textToFind.replace(" ", "%20")
    link_extractInformation = f"https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?newsearch=true&queryText={textFormat}&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&rowsPerPage=100&pageNumber={pageNumber}"
    return link_extractInformation


def createLinkExtractInformation_sage(pageNumber, textToFind: str):
    textFormat = textToFind.replace(" ", "%20")
    link_extractInformation = f"https://journals-sagepub-com.crai.referencistas.com/action/doSearch?field1=AllField&text1={textFormat}&publication=&Ppub=&access=&pageSize=100&startPage={pageNumber}"
    return link_extractInformation


def createLinkExtractInformation_scienceDirect(textToFind: str):
    textFormat = textToFind.replace(" ", "%20")
    link_extractInformation = f"https://www-sciencedirect-com.crai.referencistas.com/search?qs={textFormat}&show=100"
    return link_extractInformation


def extract_information_IEEE(page: Page, text: str):
    # Espera hasta que la URL sea la esperada
    while not page.url.startswith(link_IEEE):
        page.wait_for_timeout(1000)  # Espera 1 segundo antes de verificar nuevamente

    # Verifica que la URL sea la esperada después del inicio de sesión
    expect(page).to_have_url(link_IEEE)

    # Navega a la página de búsqueda con el texto proporcionado
    page.goto(createLinkExtractInformation_IEEE(1, text))
    # SELECCIONAR TODAS LAS REVISTAS
    page.click(
        "#xplMainContent > div.ng-SearchResults.row.g-0 > div.col > xpl-results-list > div.results-actions.hide-mobile > label > input"
    )
    page.wait_for_timeout(10000)

    # Haz clic en el botón de exportar resultados de búsqueda
    page.click(
        "#xplMainContent > div.ng-Dashboard > div.col-12.action-bar.hide-mobile > ul > li.Menu-item.inline-flexed.export-filter.no-line-break.pe-3.myproject-export > xpl-export-search-results > button"
    )
    page.wait_for_timeout(2300)

    # SELECCIONA CITACION
    page.click(
        "body > ngb-modal-window > div > div > div.d-flex.align-items-center.border-bottom > ul > li:nth-child(2)"
    )
    page.wait_for_timeout(4000)

    # Espera a que el elemento esté visible antes de hacer clic
    page.wait_for_selector('label[for="download-bibtex"] > input', timeout=60000)
    # Selecciona la opción BibTeX
    page.click('label[for="download-bibtex"] > input')

    # Espera a que el botón de descarga esté visible antes de hacer clic
    page.wait_for_selector(
        "button.stats-SearchResults_Citation_Download.xpl-btn-primary", timeout=60000
    )
    page.click("button.stats-SearchResults_Citation_Download.xpl-btn-primary")
    page.wait_for_timeout(15000)


def extract_information_sage(page: Page, text: str):
    # Navega a la página de búsqueda con el texto proporcionado
    link = createLinkExtractInformation_sage(1, text)
    page.goto(link)

    # Espera hasta que la URL sea la esperada
    while not page.url.startswith(link):
        page.wait_for_timeout(1000)  # Espera 1 segundo antes de verificar nuevamente

    # Verifica que la URL sea la esperada después del inicio de sesión
    expect(page).to_have_url(link)

    page.click("#onetrust-accept-btn-handler")

    page.click("#action-bar-select-all")

    page.click(
        "#pb-page-content > div > div > main > div.content.search-page > div > div > div > div.search-result.doSearch > div.search-result--grid > div.search-result--grid__block.search-result--grid__block__2 > div > div.article-actionbar__btns"
    )
    page.wait_for_timeout(7000)
    page.select_option("#citation-format", "bibtex")


def extract_information_ScienceDirect(text: str):
    # Navega a la página de búsqueda con el texto proporcionado
    link = createLinkExtractInformation_scienceDirect(text)
    page.goto(link)

    # Espera hasta que la URL sea la esperada
    while not page.url.startswith(link):
        page.wait_for_timeout(1000)  # Espera 1 segundo antes de verificar nuevamente

    # Verifica que la URL sea la esperada después del inicio de sesión
    expect(page).to_have_url(link)

    page.click(
        "#srp-toolbar > div.grid.row.u-show-from-sm > span > span.result-header-controls-container > span:nth-child(1) > div"
    )
    page.click(
        "#srp-toolbar > div.grid.row.u-show-from-sm > span > span.result-header-controls-container > span.header-links-container > div.ExportAllLink.result-header-action__control.u-margin-s-left > button > span"
    )

    # Espera a que el botón de exportación BibTeX esté visible antes de hacer clic
    page.wait_for_selector(
        'button[data-aa-button="srp-export-multi-bibtex"]', timeout=60000
    )
    page.click('button[data-aa-button="srp-export-multi-bibtex"]')
    page.wait_for_timeout(15000)


def vaciarCarpeta(carpeta: str):
    # Verifica si la carpeta existe, si no, créala
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Cambia el directorio actual a la carpeta especificada
    os.chdir(carpeta)

    # Lista los archivos en la carpeta
    archivos = os.listdir()

    # Elimina cada archivo en la carpeta
    for archivo in archivos:
        os.remove(archivo)
        print(f"Archivo '{archivo}' eliminado")

    print(f"Todos los archivos en la carpeta '{carpeta}' han sido eliminados")


def test(page: Page, txt: str):
    login(page, username, password)
    extract_information_IEEE(page, txt)
    extract_information_sage(page, txt)
    extract_information_ScienceDirect(txt)
    unification()


# Run the test
with sync_playwright() as p:
    # Specify the download directory
    txt = input("Ingresa el texto que deseas buscar:\n")
    vaciarCarpeta("archivos_csv")
    browser = p.chromium.launch(headless=False, downloads_path="archivos_csv")
    page = browser.new_page()
    test(page, txt)
    browser.close()
