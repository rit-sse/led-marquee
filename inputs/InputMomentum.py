import urllib.request
import json

def get():
    """
    Returns properly formatted string for the next event
    taking place in the SSE.
    """
    next_event = ""
    event_url = "https://sse.se.rit.edu/events/current.json"
    request = urllib.request.urlopen(event_url)
    event_info = json.loads(request.read().decode("utf-8"))
    request.close

    if event_info is not None:
        next_event = str(event_info['short_name'])

    return next_event

def isFiltered():                                                               
    """                                                                         
    Returns True if it must be filtered, False otherwise.                       
    """                                                                         
    return False
