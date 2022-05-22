from typing import Type
from requests import Session
from math import trunc
from bs4 import BeautifulSoup


headers = {
    'USER-AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}

my_request = Session()
my_request.headers = headers
class Apartment:

    def __init__(
        self,
        floor_size, 
        rooms, 
        bathrooms, 
        address, 
        parking_spaces, 
        condominium, 
        iptu, 
        price):

        self.floor_size = floor_size
        self.rooms = rooms
        self.bathrooms = bathrooms
        self.address = address
        self.parking_spaces = parking_spaces
        self.condominium = condominium
        self.iptu = iptu
        self.price = price

    def __repr__(self) -> str:
        area = f'Área: {self.floor_size}\n'
        quartos = f'Quartos: {self.rooms}\n'
        banheiros = f'Banheiros: {self.bathrooms}\n'
        endereco = f'Endereço: {self.address}\n'
        garagem = f'Vagas de Garagem: {self.parking_spaces}\n'
        condominio = f'Condomínio: {self.condominium}\n'
        iptu = f'IPTU: {self.iptu}\n'
        preco = f'Preço: {self.price}'
        return (
            area
            +quartos
            +banheiros
            +endereco
            +garagem
            +condominio
            +iptu
            +preco
        )

apartments = []
for index in iter(range(1,11)):
    response = my_request.get(
        f"https://www.zapimoveis.com.br/venda/apartamentos/rj+rio-de-janeiro/?pagina={index}"
    );
    if (trunc(response.status_code/100) == 2):
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        apartment_links = (
            element.get('href') 
            for element in soup.find_all('a',{'class': 'card-listing'})
        )
        for link in apartment_links:
            html = my_request.get(link).text
            soup = BeautifulSoup(html, 'html.parser')
            floor_size = soup.find('span', {'itemprop': 'floorSize'})
            try:
                floor_size = floor_size.contents[0].replace('m²','').strip()
            except (TypeError, AttributeError):
                floor_size = None
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
            address = soup.find('span', {'class': 'link'})
            try:
                address = address.contents[0].strip()
            except (TypeError, AttributeError):
                address = None
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
            apartment = Apartment(
                floor_size,
                number_of_rooms,
                number_of_bathrooms,
                address,
                parking_spaces,
                condominium,
                iptu,
                price
            )
            apartments.append(apartment)
    else:
        if(apartments):
            print(index)
            print(apartments.length)
        else:
            raise Exception("Problema no acesso ao site")

with open('artifacts/apartamentos.csv','w') as f:
    HEADERS = 'Área;Quartos;Banheiros;Endereço;Vagas de Garagem;Condomínio;IPTU;Preço de Venda\n'
    f.write(HEADERS)
    for apartment in apartments:
        area = f'{apartment.floor_size};'
        quartos = f'{apartment.rooms};'
        banheiros = f'{apartment.bathrooms};'
        endereco = f'{apartment.address};'
        garagem = f'{apartment.parking_spaces};'
        condominio = f'{apartment.condominium};'
        iptu = f'{apartment.iptu};'
        preco = f'{apartment.price}'
        f.write(
            area
            +quartos
            +banheiros
            +endereco
            +garagem
            +condominio
            +iptu
            +preco
            +'\n'
        )
