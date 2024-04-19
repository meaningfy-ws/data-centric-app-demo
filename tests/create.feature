# Created by duprijil

Feature: Create foaf:Person, foaf:Group or foaf:Organization into the triple store

  As a user i want to create a person, a group or an organization into the triple store.
  foaf:Person, foaf:Group and foaf:Organization are the classes that are defined in the ontology FOAF.

  Scenario: Create foaf:Person that don't know anyone
    Given a person with the following properties according to ontology foaf:Person:
      | _id           | foaf:lastName | foaf:firstName | foaf:knows | foaf:age |
      | JohnsDummyURI | Doe           | John           |            | 30       |
    When the user creates the foaf:Person into the triple store
    Then the person should be in the triple store


  Scenario Outline: Create foaf:Person that knows someone
    Given a person with the following properties according to ontology foaf:Person:
      | _id           | foaf:lastName | foaf:firstName | foaf:knows      | foaf:age |
      | JohnsDummyURI | Doe           | John           | PatricsDummyURI | 32       |
    And a person with the following properties according to ontology foaf:Person:
      | _id             | foaf:lastName | foaf:firstName | foaf:knows | foaf:age |
      | PatricsDummyURI | Johnson       | Patric         |            | 30       |
    When the user creates the foaf:Person into the triple store
    Then the person should be in the triple store
    Then All <foaf:knows> should be linked to all the persons that <_id> knows

    Examples:
      | _id           | foaf:knows      |
      | JohnsDummyURI | PatricsDummyURI |

  Scenario: Create foaf:Group that don't have any members
    Given a group with the following properties according to ontology foaf:Group:
      | _id           | foaf:name | foaf:member |
      | GroupDummyURI | Group1    |             |
    When the user creates the foaf:Group into the triple store
    Then the group should be in the triple store

  Scenario Outline: Create foaf:Group that have members
    Given a group with the following properties according to ontology foaf:Group:
      | _id           | foaf:name | foaf:member   |
      | GroupDummyURI | Group1    | JohnsDummyURI |
    When the user creates the foaf:Group into the triple store
    Then the group should be in the triple store
    Then All <foaf:member>'s should exist in the triple store

    Examples:
      | foaf:member   |
      | JohnsDummyURI |

  Scenario: Create foaf:Organization that don't have any members
    Given an organization with the following properties according to ontology foaf:Organization:
      | _id         | foaf:name | foaf:member |
      | OrgDummyURI | Org1      |             |
    When the user creates the foaf:Organization into the triple store
    Then the organization should be created into the triple store according to it ontology

  Scenario Outline: Create foaf:Organization that have members
    Given an organization with the following properties according to ontology foaf:Organization:
      | _id         | foaf:name | foaf:member |
      | OrgDummyURI | Org1      | <_id>       |
    When the user creates the foaf:Organization into the triple store
    Then the organization should be created into the triple store according to it ontology
    Then  All <foaf:member>'s should exist in the triple store

    Examples:
      | _id           |
      | GroupDummyURI |
      | JohnsDummyURI |