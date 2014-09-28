from httmock import all_requests, HTTMock, response, urlmatch
import requests
import app
import json

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


@all_requests
def companies(url, request):
    headers = {'content-type': 'application/json'}
    content = {
                "metadata": {
                    "image_path_prefix": "http://images.crunchbase.com/",
                    "www_path_prefix": "http://www.crunchbase.com/",
                    "api_path_prefix": "http://api.crunchbase.com/v/2/",
                    "version": 2
                },
                "data": {
                    "paging": {
                        "items_per_page": 1000,
                        "current_page": 1,
                        "number_of_pages": 260,
                        "next_page_url": "http://api.crunchbase.com/v/2/organizations?organization_types=company&page=2",
                        "prev_page_url": "",
                        "total_items": 259707,
                        "sort_order": "custom"
                    },
                    "items": [
                        {
                            "updated_at": 1411892082,
                            "created_at": 1398010616,
                            "path": "organization/google",
                            "name": "Google",
                            "type": "Organization"
                        }
                    ]
                }
            }
    return response(200, content, headers,
            None, 5, request)

@all_requests
def products(url, request):
    headers = {'content-type': 'application/json'}
    content = json.load(open('test_products.json'))
    return response(200, content, headers, 
            None, 5, request)

def test_error():
    with HTTMock(error):
        result = app.get_endpoint('organizations')
        assert result != None
        assert result == []

def test_no_results():
    with HTTMock(no_results):
        result = app.get_endpoint('organizations')
        assert result != None
        assert result == []

def test_companies():
    with HTTMock(companies):
        result = app.get_endpoint('organizations')
        assert result != None
        assert result != []
        assert len(result) == 1
        assert result[0]['name'] == "Google"
        assert result[0]['path'] == 'organization/google'


def test_products():
    with HTTMock(products):
        result = app.get_endpoint('products')
        assert result != None
        assert result != []
        assert len(result) == 1000
        assert result[0]['name'] == "Longmire Robert Taylor Leather Coat"
        assert result[0]['path'] == 'product/longmire-robert-taylor-leather-coat'
        assert result[999]['name'] == 'FitLine'

