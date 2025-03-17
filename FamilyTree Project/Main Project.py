from datetime import date
from collections import defaultdict

class PersonBase:
    """Base class for all people in the family tree."""
    def __init__(self, name, birth_date):
        self._name = name  # Name of the person
        self._birth_date = birth_date  # Birth date of the person
        self._parents = []  # List of parents
        self._children = []  # List of children
        self._spouse = None  # Spouse, if any

    @property
    def name(self):
        return self._name

    @property
    def birth_date(self):
        return self._birth_date

    @property
    def parents(self):
        return self._parents

    @property
    def children(self):
        return self._children

    @property
    def spouse(self):
        return self._spouse

    @spouse.setter
    def spouse(self, spouse):
        """Set spouse with reciprocal linking."""
        self._spouse = spouse
        spouse._spouse = self  # Automatically link the other way

    def __str__(self):
        """Human-readable representation of a person."""
        return self.name

    # Methods to set parents and children dynamically
    def set_parents(self, parents):
        """Set parents for this person."""
        self._parents = parents
        for parent in parents:
            parent._children.append(self)  # Link this person as a child to each parent

    def set_children(self, children):
        """Set children for this person."""
        self._children = children
        for child in children:
            child._parents.append(self)  # Link this person as a parent to each child

    def display_details(self):
        raise NotImplementedError("This method should be implemented in subclasses")


class LivingPerson(PersonBase):
    """Subclass representing a living person."""
    def display_details(self):
        """Details include that the person is alive."""
        return f"Name: {self.name}, Birth Date: {self.birth_date} (Alive)"


class DeceasedPerson(PersonBase):
    """Subclass representing a deceased person."""
    def __init__(self, name, birth_date, death_date):
        super().__init__(name, birth_date)
        self._death_date = death_date  # Date of death for the person

    @property
    def death_date(self):
        return self._death_date

    def display_details(self):
        """Details include both birth and death dates."""
        return f"Name: {self.name}, Birth Date: {self.birth_date}, Death Date: {self.death_date}"

class FamilyTree:
    """Class to manage family tree relationships and provide feature functionalities."""
    def __init__(self):
        self.members = {}  # Dictionary to store all family members by name

    def get_person(self, name):
        """Retrieve a person from the family tree by name."""
        return self.members.get(name, None)

    def get_member_details(self, name):
        """Display details about a member using polymorphism."""
        person = self.get_person(name)
        if person:
            return person.display_details()
        return "Person not found."

    # Relationship Methods
    def find_parents(self, person):
        return person.parents

    def find_grandparents(self, person):
        grandparents = []
        for parent in person.parents:
            grandparents.extend(parent.parents)
        return grandparents

    def find_siblings(self, person):
        siblings = set()
        for parent in person.parents:
            siblings.update(parent.children)
        siblings.discard(person)  # Exclude the person themselves
        return list(siblings)

    def find_cousins(self, person):
        cousins = []
        for parent in person.parents:
            for sibling in self.find_siblings(parent):  # Parents' siblings
                cousins.extend(sibling.children)  # Children of parents' siblings
        return cousins

    def find_immediate_family(self, person):
        immediate_family = set()
        immediate_family.update(person.parents)
        immediate_family.update(self.find_siblings(person))
        if person.spouse:
            immediate_family.add(person.spouse)
        immediate_family.update(person.children)
        return list(immediate_family)

    def find_extended_family(self, person):
        extended_family = set()
        extended_family.update(self.find_immediate_family(person))  # Start with immediate family
        for parent in person.parents:
            for sibling in self.find_siblings(parent):  # Aunts/Uncles
                extended_family.add(sibling)
                extended_family.update(sibling.children)  # Cousins
        # Filter only living relatives
        return [member for member in extended_family if isinstance(member, LivingPerson)]

    def get_birthdays_calendar(self):
        birthday_calendar = defaultdict(list)
        for person in self.members.values():
            if person.birth_date:
                birthday_calendar[(person.birth_date.month, person.birth_date.day)].append(person.name)
        return dict(sorted(birthday_calendar.items()))

    def calculate_average_age(self):
        total_age = 0
        count = 0
        for person in self.members.values():
            if isinstance(person, DeceasedPerson):  # Only deceased persons have age at death
                age_at_death = (person.death_date - person.birth_date).days // 365
                total_age += age_at_death
                count += 1
        return total_age / count if count > 0 else 0

    def calculate_children_statistics(self):
        total_children = 0
        num_people = len(self.members)
        children_data = {}

        for person in self.members.values():
            children_count = len(person.children)
            children_data[person.name] = children_count
            total_children += children_count

        average_children = total_children / num_people if num_people > 0 else 0
        return children_data, average_children

# Initialize FamilyTree
family_tree = FamilyTree()

# Create living and deceased persons
cornelia = LivingPerson("Cornelia Emmersohn", date(1968, 5, 20))
otto = DeceasedPerson("Otto Emmersohn", date(1965, 8, 15), date(2020, 4, 10))
anna = DeceasedPerson("Anna Singh", date(1945, 4, 10), date(2015, 3, 20))
raj = DeceasedPerson("Raj Singh", date(1942, 6, 5), date(2010, 11, 5))
maria = DeceasedPerson("Maria Müller", date(1943, 6, 5), date(2005, 9, 15))
hans = DeceasedPerson("Hans Emmersohn", date(1940, 3, 22), date(2012, 7, 10))
child1 = LivingPerson("Lucas Emmersohn", date(1992, 11, 12))
child2 = LivingPerson("Emma Emmersohn", date(1995, 2, 28))

# Set relationships using set_parents and set_children
cornelia.set_parents([anna, raj])
otto.set_parents([maria, hans])

cornelia.set_children([child1, child2])
otto.set_children([child1, child2])

# Set spouse relationships
cornelia.spouse = otto

# Add members directly to the family tree
family_tree.members = {
    cornelia.name: cornelia,
    otto.name: otto,
    anna.name: anna,
    raj.name: raj,
    maria.name: maria,
    hans.name: hans,
    child1.name: child1,
    child2.name: child2
}

def display_menu():
    print("\n--- Family Tree Menu ---")
    print("1. View Member Details")
    print("2. View Parents")
    print("3. View Grandparents")
    print("4. View Immediate Family")
    print("5. View Extended Family")
    print("6. View Siblings")
    print("7. View Cousins")
    print("8. View Birthday Calendar")
    print("9. View Average Age at Death")
    print("10. View Number of Children and Average Children per Person")
    print("11. Exit")

def handle_choice(choice):
    match choice:
        case "1":  # View Member Details
            name = input("Enter the name of the person: ")
            print(family_tree.get_member_details(name))

        case "2":  # View Parents
            name = input("Enter the name of the person: ")
            person = family_tree.get_person(name)
            if person:
                parents = family_tree.find_parents(person)
                print(f"Parents of {name}: {[str(parent) for parent in parents]}")
            else:
                print("Person not found.")

        case "3":  # View Grandparents
            name = input("Enter the name of the person: ")
            person = family_tree.get_person(name)
            if person:
                grandparents = family_tree.find_grandparents(person)
                print(f"Grandparents of {name}: {[str(grandparent) for grandparent in grandparents]}")
            else:
                print("Person not found.")

        case "4":  # View Immediate Family
            name = input("Enter the name of the person: ")
            person = family_tree.get_person(name)
            if person:
                immediate_family = family_tree.find_immediate_family(person)
                print(f"Immediate Family of {name}: {[str(member) for member in immediate_family]}")
            else:
                print("Person not found.")

        case "5":  # View Extended Family
            name = input("Enter the name of the person: ")
            person = family_tree.get_person(name)
            if person:
                extended_family = family_tree.find_extended_family(person)
                print(f"Extended Family of {name}: {[str(member) for member in extended_family]}")
            else:
                print("Person not found.")

        case "6":  # View Siblings
            name = input("Enter the name of the person: ")
            person = family_tree.get_person(name)
            if person:
                siblings = family_tree.find_siblings(person)
                print(f"Siblings of {name}: {[str(sibling) for sibling in siblings]}")
            else:
                print("Person not found.")

        case "7":  # View Cousins
            name = input("Enter the name of the person: ")
            person = family_tree.get_person(name)
            if person:
                cousins = family_tree.find_cousins(person)
                print(f"Cousins of {name}: {[str(cousin) for cousin in cousins]}")
            else:
                print("Person not found.")

        case "8":  # View Birthday Calendar
            print("Family Birthday Calendar:")
            birthday_calendar = family_tree.get_birthdays_calendar()
            for date, names in birthday_calendar.items():
                print(f"{date[1]:02d}/{date[0]:02d}: {', '.join(names)}")

        case "9":  # View Average Age at Death
            avg_age = family_tree.calculate_average_age()
            print(f"The average age at death is: {avg_age:.2f} years")

        case "10":  # View Number of Children and Average Children per Person
            children_data, avg_children = family_tree.calculate_children_statistics()
            print("Number of children per individual:")
            for name, count in children_data.items():
                print(f"{name}: {count}")
            print(f"The average number of children per person is: {avg_children:.2f}")

        case "11":  # Exit
            print("Exiting the program. Goodbye!")
            return False

        case _:  # Invalid Choice
            print("Invalid choice. Please try again.")

    return True


def main():
    while True:
        display_menu()
        if not handle_choice(input("Enter your choice: ")):
            break

if __name__ == "__main__":
    main()
