import urllib.request
import json
from datetime import datetime
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

    time = (str(event_info['end_date'])[11:-6])                                 
    date = (str(event_info['end_date'])[0:10])                                  
    checkAgainstTime = datetime.now().strftime('%H:%M:%S')                      
    checkAgainstDate = datetime.now().strftime('%Y-%m-%d')                      
    if event_info is not None and date <= checkAgainstDate and time > checkAgainstTime:
        next_event = "Next Event: " + str(event_info['short_name'] + "\n") 
    else:                                                                       
        next_event = "" 
    return next_event  
def isFiltered():                                                               
    """                                                                         
    Returns True if it must be filtered, False otherwise.                       
    """                                                                         
    return False
