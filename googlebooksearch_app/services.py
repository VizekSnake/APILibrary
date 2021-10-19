from googleapiclient.discovery import build
import json


def get_books_data(query):
    """Retriving data from google books API"""

    service = build('books',
                    'v1',
                    developerKey='AIzaSyDk5GTU_eBOBPVRU7QLDI2CzEbRbeAvZiI'
                    )
    request = service.volumes().list(q=query)
    response = request.execute()
    book_list = [response['items'][item]['volumeInfo']
                 for item in range(len(response['items']))]

    return book_list
