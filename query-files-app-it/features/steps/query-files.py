from behave import *


# https://jenisys.github.io/behave.example/tutorials/tutorial10.html
#
# -- REGISTER: User-defined type converter (parse_type).
# Let's parse "Int" as is int.
register_type(Int=lambda param: int(param))


# -- REGISTER: User-defined type converter (parse_type).
# Let's parse "Text" as is.
register_type(Text=lambda param: param)


@given(u'There are "{files_count:Int}" files in domain "{domain_name:Text}"')
def step_impl(context, files_count, domain_name):
    pass


@when(u'I query for files from domain matching regexp "{domain_regexp:Text}"')
def step_impl(context, domain_regexp):
    pass


@then(u'I receive "{files_count:Int}" files from domain "{domain_name:Text}"')
def step_impl(context, files_count, domain_name):
    pass


@then(u'I receive no other files')
def step_impl(context):
    pass
