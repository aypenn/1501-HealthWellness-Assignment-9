from datetime import date
class Owner:
    def __init__(self, id : str, first_name : str, last_name : str, street_address:str, city:str, state:str, zipcode:str, dob : date):
        self.__id = id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__street_address = street_address
        self.__city = city
        self.__state = state
        self.__zipcode = zipcode
        self.__dob = dob

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def full_name(self):
        return self.__first_name + " " + self.__last_name

    @property
    def address(self):
        return f"{self.__street_address}\n{self.__city}, {self.__state} {self.__zipcode}"

    @property
    def first_name(self):
        return self.__first_name
    @first_name.setter
    def first_name(self, value):
        self.__first_name = value
    @property
    def last_name(self):
        return self.__last_name
    @last_name.setter
    def last_name(self, value):
        self.__last_name = value
    @property
    def street_address(self):
        return self.__street_address
    @street_address.setter
    def street_address(self, value):
        self.__street_address = value
    @property
    def city(self):
        return self.__city
    @city.setter
    def city(self, value):
        self.__city = value
    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, value):
        self.__state = value
    @property
    def zipcode(self):
        return self.__zipcode
    @zipcode.setter
    def zipcode(self, value):
        self.__zipcode = value
    @property
    def date_of_birth(self):
        return self.__dob
    @date_of_birth.setter
    def date_of_birth(self, value : date):
        self.__dob = value

    def to_dict(self):
        return {"id": self.id, "first_name": self.first_name, "last_name": self.last_name, "street_address": self.street_address,
                "city": self.city, "state": self.state, "zipcode": self.zipcode, "dob": self.__dob.strftime("%m-%d-%Y")}

    def __eq__(self, other):
        return isinstance(other, Owner) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"ID: {self.id}\nOwner Name: {self.first_name} {self.last_name}\nAddress: {self.__street_address}         \n" \
        f"{self.city}, {self.state} {self.zipcode} \nDOB: {self.date_of_birth}"
