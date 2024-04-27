from src.adapters.fuseki_repository import PersonFusekiRepository
from src.adapters.graphpdb_repository import PersonGraphDBRepository
from src.models.foaf import Person, PersonSchema

fuseki_host = "http://localhost:3030"
graphdb_host = "http://localhost:7200"
fuseki_repo_name = "ds"
graphdb_repo_name = "test"

if __name__ == '__main__':
    person_john = Person(id="http://example.com/person/JohnsDummyURI",
                         first_name="John",
                         last_name="Doe",
                         knows=None,
                         age=50
                         )

    person_anton = Person(id="http://example.com/person/AntonsDummyURI",
                          first_name="Anton",
                          last_name="Priton",
                          knows=[person_john],
                          age=25
                          )


    fuseki_repo = PersonFusekiRepository(endpoint_url=fuseki_host, graph_name=fuseki_repo_name)
    graphdb_repo = PersonGraphDBRepository(host=graphdb_host, repo_name=graphdb_repo_name)

    new_john_from_fuskei = fuseki_repo.get(person_john.id)
    new_john_from_graphdb = graphdb_repo.get(person_john.id)

