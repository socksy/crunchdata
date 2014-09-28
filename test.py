from httmock import all_requests, HTTMock, response
import requests
import app

@all_requests
def error(url, request):
    headers = {'content-type': 'application/json'}
    content = {
            "data": {
                "response": "false",
                "error": {
                    "message": "Cannot GET to https://A0EF2HAQR0-2.algolia.io/1/indexes/organization_production?query=&&facets=%2A&hitsPerPage=1000&attributesToRetrieve=%5B%22name%22%2C%22url%22%2C%22created_at%22%2C%22updated_at%22%2C%22type%22%5D&facetFilters=%5B%22primary_role%3Acompany%22%5D&page=-1: {\"message\":\"Invalid value for page parameter\"}\n (400)",
                    "code": 500
                    }
                }
            }
    #yes, in the case of an error it still returns 200
    return response(200, content, headers, 
            None, 5, request)


@all_requests
def no_results(url, request):
    headers = {'content-type': 'application/json'}
    content = {
            "data": {
                "metadata": {},
                "paging": {},
                "items": []
                }
            }
    return response(200, content, headers, 
            None, 5, request)


def test_error():
    with HTTMock(error):
        print(app.get_endpoint('organizations'))

def test_no_results():
    with HTTMock(no_results):
        result = app.get_endpoint('organizations')
        assert result != None
        assert result == []
