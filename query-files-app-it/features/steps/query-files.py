from behave import *

from behave import register_type


# https://jenisys.github.io/behave.example/tutorials/tutorial10.html
#
def parse_number(text):
    """
    Convert parsed text into a number.
    :param text: Parsed text, called by :py:meth:`parse.Parser.parse()`.
    :return: Number instance (integer), created from parsed text.
    """
    return int(text)


# -- REGISTER: User-defined type converter (parse_type).
register_type(Number=parse_number)


def parse_text(text):
    return text


# -- REGISTER: User-defined type converter (parse_type).
register_type(Text=parse_text)


@given(u'There are "{files_count:Number}" files in domain "{domain_name:Text}"')
def step_impl(context, files_count, domain_name):
    pass


@when(u'I query for files from domain matching regexp "{domain_regexp:Text}"')
def step_impl(context, domain_regexp):
    pass


@then(u'I receive "{files_count:Number}" files from domain "{domain_name:Text}"')
def step_impl(context, files_count, domain_name):
    pass


@then(u'I receive no other files')
def step_impl(context):
    pass
