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