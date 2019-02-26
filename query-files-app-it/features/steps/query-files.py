from behave import *
import requests

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
    assert files_count == len(context.files_existing_in_domains[domain_name])


@when(u'I query for files from domain matching regexp "{domain_regexp:Text}"')
def step_impl(context, domain_regexp):
    # Let's load files matching domain regexp.
    url = context.query_files_app_url + '/v1/files?read_domain_regex=' + domain_regexp
    r = requests.get(url)
    r.raise_for_status()

    # Store the returned files in the context for the next steps.
    context.returned_files = r.json()

    # @TODO better logging
    print(f"Received result from HTTP request to query-files-app: {context.returned_files}")


@then(u'I receive "{files_count:Int}" files from domain "{domain_name:Text}"')
def step_impl(context, files_count, domain_name):
    # Domain names in s3 are always lower case.
    s3_domain_name = domain_name.lower()

    # Check whether domain is returned at all
    assert s3_domain_name in context.returned_files, f"Domain '{domain_name}' was not returned at all"

    # Let's remove the selected domain from the result kept in context. (so that other steps do not see it)
    returned_domain_files = context.returned_files.pop(s3_domain_name)
    # Let's assure that domain contained expected number of files.
    assert files_count == len(returned_domain_files)

    if files_count < 1:
        # Nothing more to check.
        return

    # Let's assure that domain contained expected files.
    expected_files = context.files_existing_in_domains[domain_name]
    returned_files_set = set(returned_domain_files)
    for file_name in expected_files:
        if file_name in returned_files_set:
            returned_files_set.discard(file_name)
        else:
            raise NotImplementedError(f"@TODO: how to fail ?: Error. File {file_name} was not returned from domain {domain_name}.")
    # Let's assure that no more files were returned for this domain.
    assert 0 == len(returned_files_set), f"Expected: {{}}, Actual: {returned_files_set}"


@then(u'I receive no other files')
def step_impl(context):
    # Let's check that we have processed all the returned files, i.e. there is no domain in the result kept in context.
    assert 0 == len(context.returned_files.keys()), f"Expected: {{}}, Actual: {context.returned_files}"
