import requests

def get_book_details(book_name):
    '''Call openlibrary api and fetch required details'''
    url = "https://openlibrary.org/search.json"
    params = {
        "title": book_name,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # The 'docs' field contains the list of books found
        resp_json = {
                'status':True,
                'books':[]
            }
        for book in data['docs']:
            book_details = {
                "title":book.get('title'),
                "author_name":book.get('author_name', []),
                "number_of_pages":book.get('number_of_pages', book.get('number_of_pages_median', 0))
            }
            resp_json['books'].append(book_details)
        return resp_json
    else:
        return {
                'status':False,
                'books':[]
            }