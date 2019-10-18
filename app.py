import owlready2 as owl

from flask import Flask
from flask_restful import Resource, Api, reqparse
from create_ontology import onto

app = Flask(__name__)
api = Api(app)

onto = owl.get_ontology("onto.owl").load()


def find_entities(name, class_type):
    return [c.to_json() for c in
            onto.search(type=class_type, iri="*{}*".format(name))]


def find_entity(name, class_type):
    entities = [c for c in
                onto.search(type=class_type, iri="*#{}".format(name))]
    return entities[0] if entities else None


class CompanyAPI(Resource):
    def get(self, name):
        companies = find_entities(name, onto.Company)
        if companies:
            return companies, 200

        return "Company not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("industry")
        parser.add_argument("founder")
        args = parser.parse_args()

        company = find_entity(name, onto.Company)
        if company:
            return "Company {} already exists.".format(name), 400

        new_company = onto.Company(name)
        if args["industry"]:
            industry = find_entity(args["industry"], onto.Industry)
            if industry:
                new_company.has_industry.append(industry)
        if args["founder"]:
            founder = find_entity(args["founder"], onto.Person)
            if industry:
                new_company.has_founder.append(founder)
        onto.save(file="onto.owl", format="ntriples")

        return new_company.to_json(), 201

    def delete(self, name):
        company = find_entity(name, onto.Company)
        if company:
            owl.destroy_entity(company)
            onto.save(file="onto.owl", format="ntriples")
            return "OK", 200

        return "Company not found", 404


class PersonAPI(Resource):
    def get(self, name):
        people = find_entities(name, onto.Person)
        if people:
            return people, 200

        return "Person not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("founder_of")
        args = parser.parse_args()

        person = find_entity(name, onto.Person)
        if person:
            return "Person {} already exists.".format(name), 400

        new_person = onto.Person(name)
        if args["founder_of"]:
            company = find_entity(args["founder_of"], onto.Company)
            if company:
                new_person.is_founder_of.append(company)
        onto.save(file="onto.owl", format="ntriples")

        return new_person.to_json(), 201

    def delete(self, name):
        person = find_entity(name, onto.Person)
        if person:
            owl.destroy_entity(person)
            onto.save(file="onto.owl", format="ntriples")
            return "OK", 200

        return "Person not found", 404


class IndustryAPI(Resource):
    def get(self, name):
        industries = find_entities(name, onto.Industry)
        if industries:
            return industries, 200

        return "Industry not found", 404

    def post(self, name):
        industry = find_entity(name, onto.Industry)
        if industry:
            return "Industry {} already exists.".format(name), 400

        new_industry = onto.Industry(name)

        return new_industry.to_json(), 201

    def delete(self, name):
        industry = find_entity(name, onto.Industry)
        if industry:
            owl.destroy_entity(industry)
            onto.save(file="onto.owl", format="ntriples")
            return "OK", 200

        return "Industry not found", 404


class OntologyAPI(Resource):
    def get(self):
        try:
            with open("onto.owl", "r") as f:
                return f.read(), 200
        except IOError:
            return "Could not read file onto.owl", 400


api.add_resource(CompanyAPI, "/company/<string:name>")
api.add_resource(PersonAPI, "/person/<string:name>")
api.add_resource(IndustryAPI, "/person/<string:name>")
api.add_resource(OntologyAPI, "/onto")
app.run(debug=True)
