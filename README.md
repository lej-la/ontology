### Assignment: Simple Ontology
In Python (or Java), define a simple ontology/taxonomy (up to 5 classes, up to 10 individuals) about companies. 
Provide REST endpoints
- to add a new individual;
- to remove an existing individual from the ontology;
- to download modified ontology.

#### Ontology design:
The proposed ontology contains three classes:  
- **Company, Industry and Person**

The following properties are allowed:
- **has_industry**_(Company, Industry)_  
- **has_founder**_(Company, Person)_  
- **is_founder_of**_(Person, Company)_

#### Init ontology:
```
python3 create_ontology.py
```

Defines the ontology, creates a few entities and saves it in `onto.owl`

#### Inspecting an entity:
We can inspect an entity by sending a GET request with the following format:
```
curl --request GET --url http://127.0.0.1:5000/<class>/<name>
```

For example, we can see details about Apple Inc. company:

```
curl --request GET --url http://127.0.0.1:5000/company/Apple_Inc
```

Simple search works, too:

```
curl --request GET --url http://127.0.0.1:5000/company/Apple
```

#### Adding an entity:
We can add a new entity by sending a POST request. 
```
curl --request POST --url http://127.0.0.1:5000/person/Albert_Einstein
```

We can also pass parameters in the following way:
```
curl --request POST --url http://127.0.0.1:5000/person/Henry?founder_of=Henry_s_Fresh_Apples
curl --request POST --url http://127.0.0.1:5000/company/IBM?industry=Computer_Hardware
```

#### Deleting an entity
```
curl --request DELETE --url http://127.0.0.1:5000/person/Albert_Einstein
```

#### Download the modified ontology in ntriples format:
```
curl --request GET --url http://127.0.0.1:5000/onto > modified_onto.owl
```
