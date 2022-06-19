import asyncio
from typing import List, Type
from aiohttp import ClientResponse, ClientSession
from math import trunc
from bs4 import BeautifulSoup
from utils import *
from models import *
from config import *

async def fetch(session:ClientSession, url:str) -> ClientResponse:
    async with session.get(url) as result:
        return result

async def get_links(session:ClientSession, urls:List[str]) -> List[str]:
    pending = [asyncio.create_task(fetch(session, url)) for url in urls]
    links = []
    while pending:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        for done_task in done:
            response = await done_task
            if (response.ok):
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                anchors = soup.find_all('a', {'class': 'card-listing'})
                apartment_links = [element.get('href') for element in anchors]
                links.extend(apartment_links)
            else:
                raise Exception("Problema no acesso ao site")
    return links

async def get_apartments(session:ClientSession, urls:List[str]) -> List[Apartment]:
    pending = [asyncio.create_task(fetch(session, url)) for url in urls]
    apartments = []
    while pending:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        for done_task in done:
            tasks = []
            response = await done_task  
            if (response.ok):
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                tasks.append(asyncio.to_thread(get_floor_size, soup))
                tasks.append(asyncio.to_thread(get_number_of_rooms, soup))
                tasks.append(asyncio.to_thread(get_number_of_bathrooms, soup))
                tasks.append(asyncio.to_thread(get_address, soup))
                tasks.append(asyncio.to_thread(get_parking_spaces, soup))
                tasks.append(asyncio.to_thread(get_condominium, soup))
                tasks.append(asyncio.to_thread(get_iptu, soup))
                tasks.append(asyncio.to_thread(get_price, soup))
                floor_size,number_of_rooms,number_of_bathrooms,address,parking_spaces,condominium,iptu,price = await asyncio.gather(*tasks)
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
                raise Exception("Problema no acesso ao site")
    return apartments

async def main():
    client = ClientSession(
        headers={'USER-AGENT': config['USER-AGENT']}
    )
    urls = (f'https://www.zapimoveis.com.br/venda/apartamentos/rj+rio-de-janeiro/?pagina={index}' for index in range(1,11))
    async with client as session:
        links = await get_links(session, urls)
        apartments = await get_apartments(session, links)

    with open('artifacts/apartamentos.csv','w') as f:
        HEADERS = 'Área;Quartos;Banheiros;Endereço;Vagas de Garagem;Condomínio;IPTU;Preço de Venda\n'
        f.write(HEADERS)
        for apartment in apartments:
            area = f'{apartment.floor_size}'
            quartos = f'{apartment.rooms}'
            banheiros = f'{apartment.bathrooms}'
            endereco = f'{apartment.address}'
            garagem = f'{apartment.parking_spaces}'
            condominio = f'{apartment.condominium}'
            iptu = f'{apartment.iptu}'
            preco = f'{apartment.price}'
            f.write(
                ';'.join((area
                    ,quartos
                    ,banheiros
                    ,endereco
                    ,garagem
                    ,condominio
                    ,iptu
                    ,preco
                    ,'\n')
                )
            )
    return None

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
                

                
                

