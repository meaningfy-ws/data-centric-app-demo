from SPARQLBurger.SPARQLQueryBuilder import SPARQLSelectQuery, SPARQLGraphPattern
from SPARQLBurger.SPARQLSyntaxTerms import Triple, Filter
from rdflib import Graph, BNode
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore, _node_to_sparql

from src.adapters.repository import PersonAbstractRepository
from src.models.foaf import Person, PersonSchema, vocab

DEFAULT_PREDICATE_NAME = '?p'
DEFAULT_SUBJECT_NAME = '?s'
DEFAULT_OBJECT_NAME = '?o'
DEFAULT_SPARQL_TRIPLE = Triple(subject=DEFAULT_SUBJECT_NAME,
                               predicate=DEFAULT_PREDICATE_NAME,
                               object=DEFAULT_OBJECT_NAME)


def my_bnode_ext(node):
    if isinstance(node, BNode):
        return '<bnode:b%s>' % node
    return _node_to_sparql(node)


context = {"@vocab": vocab}


class PersonFusekiRepository(PersonAbstractRepository):
    def __init__(self, endpoint_url: str, graph_name: str):
        self.query_endpoint = f"{endpoint_url}/{graph_name}/sparql"
        self.update_endpoint = f"{endpoint_url}/{graph_name}/update"
        self.store = SPARQLUpdateStore(node_to_sparql=my_bnode_ext)
        self.store.open((self.query_endpoint, self.update_endpoint))

    def add(self, person: Person):
        if self.get(person.id) is not None:
            print("This person already exists in the graph.")
            return

        jsonld_dict = PersonSchema().dump(person, many=True)
        graph = Graph(store=self.store)
        graph.parse(data=jsonld_dict, format='json-ld')

    def get(self, person_id: str) -> Person:
        select_query = SPARQLSelectQuery(distinct=True)
        graph_pattern = SPARQLGraphPattern()
        graph_pattern.add_triples(triples=[DEFAULT_SPARQL_TRIPLE])
        graph_pattern.add_filter(filter=Filter(
            expression=f'{DEFAULT_SUBJECT_NAME} = <{person_id}>'
        ))
        select_query.set_where_pattern(graph_pattern)
        try:
            query_result = self.store.query(select_query.get_text())
        except ValueError as e:
            print(e)
            return None
        serialization_graph = Graph()
        [serialization_graph.add(triple) for triple in query_result]
        if len(serialization_graph) == 0:
            print("This person does not exist in the graph.")
            return None
        result_ser = serialization_graph.serialize(format="json-ld", context=context)
        print("----------------Fuseki------------------")
        print(result_ser)
        print("----------------EndFuseki------------------")
        return PersonSchema().loads(result_ser)
