from multiprocessing.sharedctypes import Value
from time import process_time_ns
from urllib import response
from xmlrpc.client import ResponseError
import requests
import json 
import pprint

#Program: API Get and Post
#Programmer: Joshua Lindquist

#Defining the function to get from the API
def invoke_http_Get(url:str) -> None:
    #storing the url brought in as an arg 
    response = requests.get(url)
    #Printing the response status code to determine if it was successful
    print(response.status_code)
    if not response.ok:
        raise ValueError('The API call failed')
    #printing the data returned from the API
    obj = response.json()
    if isinstance(obj,list):
        for res in obj:
            print(res['userId'])
            print(res['id'])
            print(res['title'])
            print(res['body'])

def invoke_HTTP_Post(url:str) -> None:
    #Creating the data the will be posted from the API
    data = {'title':'Python Requests', 'body':'Test' , 'userId':'726'}
    #Storing the url and the data
    response = response.post(url, data)
    print(response.status_code)

    if not response.ok:
        raise ValueError('The API failed')
    #Pretty print with indent
    pp =pprint.PrettyPrinter(indent=2)
    pp.pprint(response.json())
    obj = response.json()
    print(obj['userId'])
    print(obj['id'])
    print(obj['title'])
    print(obj['body'])


if __name__ == "__main__":
    #Calling the get function targeted at jsonplaceholder
    try:
        url = "https://jsonplaceholder.typicode.com/posts"
        invoke_http_Get(url)
    except ValueError:
        print("The API had an error")
        
#Calling the post function targeted at jsonplaceholder
    try:
        url = "https://jsonplaceholder.typicode.com/posts"
        invoke_HTTP_Post(url)
    except ValueError:
        print("The API Posting had an error")
        
