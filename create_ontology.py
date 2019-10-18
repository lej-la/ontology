import owlready2 as owl

# Creates an empty ontology
onto = owl.get_ontology("onto.owl")

# Defines ontology structure
with onto:
    class Company(owl.Thing):
        def to_json(self):
            return {
                "name": self.name,
                "industry": [i.name for i in self.has_industry],
                "founder": [f.name for f in self.has_founder]
            }


    class Industry(owl.Thing):
        def to_json(self):
            return {
                "name": self.name
            }


    class Person(owl.Thing):
        def to_json(self):
            return {
                "name": self.name,
                "founder_of": [i.name for i in self.is_founder_of]
            }


    class has_industry(Company >> Industry):
        pass


    class has_founder(Company >> Person):
        pass


    class is_founder_of(Person >> Company):
        inverse_property = has_founder


def init_onto():
    # Creates Industry instances
    ind_hardware = onto.Industry("Computer_Hardware")
    ind_ai = onto.Industry("Artificial_Intelligence")

    # Creates Company instance with a parameter
    com_apple = onto.Company("Apple_Inc", has_industry=[ind_hardware, ind_ai])

    # Passes a parameter to an existing instance
    per_jobs = onto.Person("Steve_Jobs")
    com_apple.has_founder.append(per_jobs)

    # Checks if inverse property was assigned
    assert com_apple in per_jobs.is_founder_of

    com_openai = onto.Company("OpenAI", has_industry=[ind_ai])
    per_musk = onto.Person("Elon_Musk", is_founder_of=[com_openai])
    com_apples = onto.Company("Henry_s_Fresh_Apples")

    # Saves ontology to a file
    onto.save(file="onto.owl", format="ntriples")


init_onto()
