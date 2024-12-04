from person import Person


class Student(Person):
    def __init__(self, *args):
        super().__init__(*args)

        self.subject = None

    def enroll(self, subject):
        self.subject = subject

    def get_full_name(self):
        if self.subject is None:
            return super().get_full_name()
        else:
            full_name = f"{self.name} {self.last_name} enrolled in {self.subject}"
            return full_name


if __name__ == "__main__":
    someone = Student('Jane', 'Doe')
    print(someone.get_full_name())
    someone.calculate_age(2000)

    someone.enroll('math')
    print(someone.get_full_name())