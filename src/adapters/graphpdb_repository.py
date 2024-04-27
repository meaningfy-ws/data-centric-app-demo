from urllib.parse import urljoin

import requests
from SPARQLBurger.SPARQLQueryBuilder import SPARQLSelectQuery, SPARQLGraphPattern
from SPARQLBurger.SPARQLSyntaxTerms import Filter
from SPARQLWrapper import SPARQLWrapper
from marshmallow import EXCLUDE
from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore, SPARQLStore

from src.adapters.fuseki_repository import DEFAULT_SPARQL_TRIPLE, DEFAULT_SUBJECT_NAME, context
from src.adapters.repository import PersonAbstractRepository
from src.models.foaf import Person, PersonSchema

class GraphDBException(Exception):
    """
        An exception when GraphDB server interaction has failed.
    """

class PersonGraphDBRepository(PersonAbstractRepository):
    def __init__(self, host: str, repo_name: str):

        self.repo_name = repo_name
        self.host = host

    def add(self, person: Person):
        if self.get(person.id) is not None:
            print("This person already exists in the graph.")
            return

        jsonld_dict = PersonSchema().dump(person)
        tmp_graph = Graph()
        tmp_graph.parse(data=jsonld_dict, format='json-ld')
        rdf_string = tmp_graph.serialize(format="turtle").encode(encoding='utf-8')
        update_url = urljoin(self.host, f"/repositories/{self.repo_name}/statements")
        headers = { "Content-Type": "text/turtle"}
        response = requests.post(url=update_url, data=rdf_string, headers=headers)
        if response.status_code != 204:
            raise GraphDBException(response.text)


    def get(self, person_id: str) -> Person:
        select_query = SPARQLSelectQuery(distinct=True)
        graph_pattern = SPARQLGraphPattern()
        graph_pattern.add_triples(triples=[DEFAULT_SPARQL_TRIPLE])
        graph_pattern.add_filter(filter=Filter(
            expression=f'{DEFAULT_SUBJECT_NAME} = <{person_id}>'
        ))
        select_query.set_where_pattern(graph_pattern)

        try:
            store = SPARQLStore()
            store.open(urljoin(self.host, f"/repositories/{self.repo_name}"))
            query_result = store.query(select_query.get_text())
        except ValueError as e:
            print(e)
            return None
        serialization_graph = Graph()
        [serialization_graph.add(triple) for triple in query_result]
        if len(serialization_graph) == 0:
            print("This person does not exist in the graph.")
            return None

        result_ser = serialization_graph.serialize(format="json-ld", context=context)
        return PersonSchema().loads(result_ser)