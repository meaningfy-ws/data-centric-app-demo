# Created by duprijil

Feature: Delete foaf:Person, foaf:Group or foaf:Organization from triple store

  As a user i want to delete a foaf:Person, foaf:Group or foaf:Organization from triple store.
  foaf:Person, foaf:Group and foaf:Organization are classes that represents a Person, Group and Organization in the FOAF ontology.

  Scenario: Delete a foaf:Person from triple store
    Given a person with the following properties according to ontology foaf:Person:
      | _id           | foaf:lastName | foaf:firstName | foaf:knows | foaf:age |
      | JohnsDummyURI | Doe           | John           |            | 30       |
    Given the user creates the foaf:Person into the triple store
    When the user deletes the person
    Then the person should not be in the triple store


  Scenario: Delete a foaf:Group from triple store
    Given a group with the following properties according to ontology foaf:Group:
      | _id            | foaf:name | foaf:member   |
      | Group1DummyURI | Group1    | JohnsDummyURI |
    Given a person with the following properties according to ontology foaf:Person:
      | _id           | foaf:lastName | foaf:firstName | foaf:knows | foaf:age |
      | JohnsDummyURI | Doe           | John           |            | 30       |
    Given the user creates the foaf:Group into the triple store
    When the user deletes the group
    Then the group should not be in the triple store
    Then the person should be in the triple store


  Scenario: Delete a foaf:Organization from triple store
    Given an organization with the following properties according to ontology foaf:Organization:
      | _id          | foaf:name | foaf:member   |
      | Org1DummyURI | Org1      | JohnsDummyURI |
    Given a group with the following properties according to ontology foaf:Group:
      | _id            | foaf:name | foaf:member   |
      | Group1DummyURI | Group1    | JohnsDummyURI |
    Given a person with the following properties according to ontology foaf:Person:
      | _id           | foaf:lastName | foaf:firstName | foaf:knows | foaf:age |
      | JohnsDummyURI | Doe           | John           |            | 30       |
    Given the user creates the foaf:Organization into the triple store
    Given the user creates the foaf:Group into the triple store
    Given the user creates the foaf:Person into the triple store
    When the user deletes the organization
    Then the organization should not be in the triple store
    Then the group should be in the triple store
    Then the person should be in the triple store