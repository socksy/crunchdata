from httmock import all_requests, HTTMock, response
import requests
import app

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

def test_get_endpoint_no_results():
    with HTTMock(no_results):
        result = app.get_endpoint('organizations')
        assert result != None
        assert result == []
