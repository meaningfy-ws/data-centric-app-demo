from behave import given, when, then

@given('a person with the following properties according to ontology foaf:Person:')
def step_impl(context):
    person_table = context.table
    raise NotImplementedError(u'STEP: Given a person with the following properties according to ontology foaf:Person:')

@when('the user creates the foaf:Person into the triple store')
@given('the user creates the foaf:Person into the triple store')
def step_impl(context):
    raise NotImplementedError(u'STEP: When/Given the user creates the foaf:Person into the triple store')

@then('the person should be in the triple store')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the person should be in the triple store')

@then('All {foaf_knows} should be linked to all the persons that {_id} knows')
def step_impl(context, foaf_knows, _id):
    raise NotImplementedError(u'STEP: And All <foaf:knows> should be linked to all the persons that <_id> knows')

@given('a group with the following properties according to ontology foaf:Group:')
def step_impl(context):
    group_table = context.table
    raise NotImplementedError(u'STEP: Given a group with the following properties according to ontology foaf:Group:')

@when('the user creates the foaf:Group into the triple store')
@given('the user creates the foaf:Group into the triple store')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the user creates the foaf:Group into the triple store')

@then('the group should be in the triple store')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the group should be in the triple store')

@then('All {foaf_member}\'s should exist in the triple store')
def step_impl(context, foaf_member):
    raise NotImplementedError(u'STEP: And All <foaf:member>\'s should exist in the triple store')

@given('an organization with the following properties according to ontology foaf:Organization:')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given an organization with the following properties according to ontology foaf:Organization:')

@when('the user creates the foaf:Organization into the triple store')
@given('the user creates the foaf:Organization into the triple store')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the user creates the foaf:Organization into the triple store')

@then('the organization should be created into the triple store according to it ontology')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the organization should be created into the triple store according to it ontology')