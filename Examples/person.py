class Person:
    def __init__(self, name, last_name):
        self.name = name
        self.last_name = last_name
        self.birth_year = None  # This is initialized when using "Calculate age"

    def get_full_name(self):
        full_name = f"{self.name} {self.last_name}"
        return full_name

    def calculate_age(self, birth_year):
        self.birth_year = birth_year
        print(f"{self.name} is {2024-birth_year} years old")

    def over_age(self):
        if self.birth_year is None:
            return "I don't know"
        if 2024 - self.birth_year > 18:
            return True
        else:
            return False


if __name__ == "__main__":
    me = Person('Aquiles', 'Carattino')
    print(me.get_full_name())
    me.calculate_age(1986)
    print(me.over_age())

    you = Person('John', 'Smith')
    print(you.over_age())
