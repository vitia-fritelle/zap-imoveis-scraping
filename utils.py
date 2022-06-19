from bs4 import BeautifulSoup

def get_floor_size(soup:BeautifulSoup):
    floor_size = soup.find('span', {'itemprop': 'floorSize'})
    try:
        floor_size = floor_size.contents[0].replace('m²','').strip()
    except (TypeError, AttributeError):
        floor_size = None
    return floor_size
def get_number_of_rooms(soup:BeautifulSoup):
    number_of_rooms = soup.find(
        'span', 
        {'itemprop': 'numberOfRooms'}
    )
    try:
        number_of_rooms = (
            number_of_rooms
            .contents[0]
            .replace('quartos','')
            .replace('quarto','')
            .strip()
        )
    except (TypeError, AttributeError):
        number_of_rooms = None
    return number_of_rooms
def get_number_of_bathrooms(soup:BeautifulSoup):
    number_of_bathrooms = soup.find(
        'span', 
        {'itemprop': 'numberOfBathroomsTotal'}
    )
    try:
        number_of_bathrooms = (
            number_of_bathrooms
            .contents[0]
            .replace('banheiros','')
            .replace('banheiro','')
            .strip()
        )
    except (TypeError, AttributeError):
        number_of_bathrooms = None
    return number_of_bathrooms
def get_address(soup:BeautifulSoup):
    address = soup.find('span', {'class': 'link'})
    try:
        address = address.contents[0].strip()
    except (TypeError, AttributeError):
        address = None
    return address
def get_parking_spaces(soup:BeautifulSoup):
    parking_spaces = soup.find('li', {'class': 'js-parking-spaces'})
    try:
        parking_spaces = (
            parking_spaces
            .span
            .contents[0]
            .replace('vagas','')
            .replace('vaga','')
            .strip()
        )
    except (TypeError, AttributeError) :
        parking_spaces = None
    return parking_spaces
def get_condominium(soup:BeautifulSoup):

    condominium = soup.find('li', {'class': 'condominium'})
    try:
        condominium_tax = condominium.span
        if (condominium_tax.contents[0] == 'não informado') :
            condominium = None
        else :
            condominium = (
                condominium_tax
                .contents[0]
                .replace('R$','')
                .replace('.','')
                .strip()
            )
    except (TypeError, AttributeError):
        condominium = None
    return condominium
def get_iptu(soup:BeautifulSoup):
    iptu = soup.find('li', {'class': 'iptu'})
    try:
        iptu_value = iptu.span
        if (iptu_value.contents[0] == 'não informado'):
            iptu = None
        else :
            iptu = (
                iptu_value
                .contents[0]
                .replace('R$','')
                .replace('.','')
                .strip()
            )
    except (TypeError, AttributeError):
        iptu = None
    return iptu
def get_price(soup:BeautifulSoup):
    price = soup.find('li',{'class','price__item--main'})
    try:
        price_business = price.strong.contents[1].strip()
        if (price_business == 'Sob consulta') :
            price = None
        else :
            price = (
                price_business
                .replace('R$','')
                .replace('.','')
                .strip()
            )
    except (TypeError, AttributeError):
        price = None
    return price