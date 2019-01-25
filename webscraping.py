from bs4 import BeautifulSoup
import requests
import re


main_url = 'http://books.toscrape.com/index.html'
source = requests.get(main_url).text
soup = BeautifulSoup(source, 'lxml')

def getURL(url):
    resultado = requests.get(url)
    soup = BeautifulSoup(resultado.text, 'html.parser')
    return(soup)

#metodo para obtener las url de cada libro
def get_urls_libros(url):

    soup = getURL(url)

    return(['/'.join(url.split('/')[:-1]) + '/' + x.div.a.get('href') for x in soup.find_all('article', class_='product_pod')])


#lista para almacenar las url de cada pagina
urls_paginas = []

paginas = [str(i) for i in range (1, 51)]

print("Recolectando urls de paginas...")
for pagina in paginas:

    pagina_sgte = 'http://books.toscrape.com/catalogue/page-' + pagina + '.html'
    if requests.get(pagina_sgte).status_code == 200:
        urls_paginas.append(pagina_sgte)

print(str(len(urls_paginas)) + ' paginas recolectadas')
print("5 primeras url: ")
print(urls_paginas[:5])

urls_libros = []

for pagina in urls_paginas:
    urls_libros.extend(get_urls_libros(pagina))

print(str(len(urls_libros)) + ' links de libros recolectados')
print("5 primeras url: ")
print(urls_libros[:5])

#listas para guardar los datos:

titulos = []
precios = []
stock = []
categorias = []
urls_covers = []
reviews = []
upcs = []
tipo_producto = []
precios_sin_tax = []
precios_con_tax = []
tax = []
disponibilidades = []
num_reviews = []

print("Recabando datos...")
#se itera por cada url de cada libro y se recaban los datos
for url in urls_libros:

    soup = getURL(url)
    titulos.append(soup.find('div', class_= re.compile('product_main')).h1.text)
    precios.append(soup.find('p', class_='price_color').text[2:])
    stock.append(re.sub("[^0-9]", "", soup.find('p', class_='instock availability').text))
    categorias.append(soup.find('a', href = re.compile('../category/books/')).get('href').split('/')[3])
    urls_covers.append(url.replace('index.html', '') + soup.find('img').get('src'))
    reviews.append(soup.find('p', class_= re.compile('star-rating')).get('class')[1])

    table = soup.find('table', class_='table table-striped')
    datos_tabla = []
    
    for tr in table.find_all('tr'):
        for td in tr.find_all('td'):
            datos_tabla.append(td.text)

    upcs.append(datos_tabla[0])
    tipo_producto.append(datos_tabla[1])
    precios_sin_tax.append(datos_tabla[2][2:])
    precios_con_tax.append(datos_tabla[3][2:])
    tax.append(datos_tabla[4][2:])
    disponibilidades.append(datos_tabla[5])
    num_reviews.append(datos_tabla[6])


import pandas as pd


datos = pd.DataFrame({'TITLE': titulos, 'PRICE': precios, 'STOCK': stock, 'CATEGORY': categorias, 'COVER': urls_covers, 'UPC': upcs, 'PRODUCT_TYPE': tipo_producto, 'PRICE (excl tax)': precios_sin_tax, 'PRICE (incl tax)': precios_con_tax, 'TAX': tax, 'AVAILABILITY': disponibilidades, 'N° OF REVIEWS': num_reviews, 'reviews': reviews})
datos.head()

print("Generando CSV...")
datos.to_csv('datos_recolectados.csv', encoding='utf-8')


