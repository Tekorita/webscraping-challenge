import requests

import pandas as pd

from bs4 import BeautifulSoup
 
url_base = 'http://books.toscrape.com/'
url_archivos = url_base + '/archivos' 
page = requests.get(url_base)
soup = BeautifulSoup(page.text, 'html.parser')

def export_csv(scrap):
    """Exportamos el json scraper en formato csv"""
    df = pd.DataFrame(scrap)
    df.to_csv('scraperBooks.csv', sep='\t', encoding='utf-8')
    print("scraper exportado a formato csv con exito   ")

def get_links():
    """Recorremos el link de cada libro"""
    href_links = []
    for href in soup.find_all(class_="image_container"):
        image = href.find('a', href=True)
        href_links.append(image['href'])
    
    return href_links

def get_content(links):
    """Extraemos el contenido de los items del libro para crear el scrapper"""
    product_infor = []
    libro = {}
    product_description = {}
    scrap_web = []

    for link in links:
        page = requests.get(url_base + link)
        soup = BeautifulSoup(page.text, 'html.parser')
        title = soup.find(class_='col-sm-6 product_main').find("h1").text
        price = soup.find(class_='col-sm-6 product_main').find(class_="price_color").text
        stock = soup.find(class_='col-sm-6 product_main').find(class_="instock availability").text
        category = soup.find(class_='breadcrumb').find_all("a")[2].text
        cover = soup.find("img")

        libro['Title'] = title
        libro['Price'] = price
        libro['Stock'] = stock.strip()
        libro['Category'] = category
        libro['Cover'] = cover['src']

        for items in soup.find(class_='table table-striped').find_all("td"):
            """Iteramos la tabla de la descripcion del productos para traer los items"""
            product_infor.append(items.getText())

            if len(product_infor) == 7:           
                product_description['UPC'] = product_infor[0]
                product_description['Product Type'] = product_infor[1]
                product_description['Price (excl. tax)'] = product_infor[2]
                product_description['Price (incl. tax)'] = product_infor[3]
                product_description['Tax'] = product_infor[4]
                product_description['Availability'] = product_infor[5]
                product_description['Number of reviews'] = product_infor[6]
                libro['Product Description'] = product_description          
                product_infor = []
                
        print(libro)  
        scrap_web.append(libro)
        print("se guardo todo el contenido de un libro en el json")
        print("---------------------------------------------------------------------------------------")
    #print(scrap_web)
    """Exportamos el scrap en formato csv"""
    export_csv(scrap_web)

urls_books = get_links()

get_content(urls_books)





