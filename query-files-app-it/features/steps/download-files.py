from behave import *
import requests
from urllib.parse import quote

# https://jenisys.github.io/behave.example/tutorials/tutorial10.html
#
# -- REGISTER: User-defined type converter (parse_type).
# Let's parse "Int" as is int.
register_type(Int=lambda param: int(param))


# -- REGISTER: User-defined type converter (parse_type).
# Let's parse "Text" as is.
register_type(Text=lambda param: param)


@when(u'I download "{files_count:Int}" files from domain "{domain_name:Text}"')
def step_impl(context, files_count, domain_name):
    # Let's store values in the context for the next steps.
    # @TODO Add support for scenario where downloading from more than one domain.
    context.download_file_domain_name = domain_name
    context.download_file_files_count = files_count

    # Note: The actual download operation is executed in the next step
    #  because that is where we do verification.


def file_download_response(context, file_number):
    """Runs HTTP GET request for a file-download resource and returns the response."""

    # We need to quote names before putting them in URL. (e.g. file names may contain '/' characters)
    # (see also: https://stackoverflow.com/questions/1695183/how-to-percent-encode-url-parameters-in-python )
    file_name_in_url = quote(context.download_file_domain_name + ':' + str(file_number), safe='')
    domain_name_in_url = quote(context.download_file_domain_name, safe='')

    # Download a file.
    url = (context.query_files_app_url
           + '/v1/file-download?read_domain_regex=' + quote(context.domain_regex, safe='')
           + f"&domain_name={domain_name_in_url}&file_name={file_name_in_url}")

    # # We need to quote names before putting them in URL. (e.g. file names may contain '/' characters)
    # # (see also: https://stackoverflow.com/questions/1695183/how-to-percent-encode-url-parameters-in-python )
    # file_name_in_url = quote(domain_name + ':' + str(file_number), safe='')
    # domain_name_in_url = quote(domain_name, safe='')
    #
    # # Download a file.
    # url = (api_url
    #        + '/v1/file-download-props?read_domain_regex=' + domain_regex
    #        + f"&domain_name={domain_name_in_url}&file_name={file_name_in_url}")
    #
    return requests.get(url)


@then(u'I receive files contents')
def step_impl(context):
    for i in range(context.download_file_files_count):
        r = file_download_response(context, i)
        r.raise_for_status()

        print(f"Received result from HTTP request to query-files-app: {r.json()}")

        # The result contains (pre-signed) URL which we use for a download request.
        download_url = r.json()['download-url']

        # Download file contents.
        file_contents_response = requests.get(download_url)
        file_contents_response.raise_for_status()

        print(f"Received result from HTTP request to query-files-app: {file_contents_response.text}")

        # Verify contents.  (Note: Every test file was created with text "something".)
        assert "something" == file_contents_response.text


@then(u'I receive no such file error')
def step_impl(context):
    for i in range(context.download_file_files_count):
        r = file_download_response(context, i)
        assert 404 == r.status_code, f"Not expected response with code: {r.status_code}"
