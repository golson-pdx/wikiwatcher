'''defines revision base class'''
from datetime import datetime
import json
import requests

# pylint: disable=R0903
class User():
    '''defines a wikipedia user by name and id number'''
    def __init__(self, name: str, id_num: int) -> None:
        self.name: str = name
        self.id_num: int = id_num

# pylint: disable=R0902
class Revision():
    '''revision object holds json revision info'''
    def __init__(self, title=None, user=None) -> None:
        # possible params
        self.json: dict = None
        self.revision_id: int = None
        self.title: str = None
        self.timestamp: datetime = None
        self.page_id: int = None
        self.user: User = None
        self.minor: bool = None
        self.tags: list[str] = None
        self.comment: str = None
        self.parent_id: int = None
        self.size: int = None

    def get_contents(self, title='None', username='None'): #start and end time stamps???
        ''' Returns the content of the page at this revision'''

        session = requests.Session()

        url = "https://www.wikipedia.org/w/api.php"

        params = {
            #params for Revisions API
            #https://www.mediawiki.org/wiki/API:Revisions
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": title,
            "rvprop": "comment|content|flags|ids|size|tags|timestamp|user|userid",
            "rvslots": "main",
            "formatversion": "2",
            #params for AllRevisions API
            #https://www.mediawiki.org/wiki/API:Allrevisions
            "arvuser": username,
            "arvprop": "comment|content|flags|ids|size|tags|timestamp|user|userid",
            "list": "allrevisions"
        }

        request = session.get(url=url, params=params)
        data = request.json()

        if title != 'None': #page history
            page_revisions = data["query"]["pages"]
            self.json = page_revisions[0] #first revision in the list

        else: #user history
            user_revisions = data["query"]["allrevisions"]
            self.json = user_revisions[0] #first revision in the list
            
        print(json.dumps(self.json, indent=1))

    def get_diff(self, to_id: int = None):
        """ Returns the difference between this revision and its parent 
        in this revision's article's history, unless a toId is specified in
        which case this revision is compared with toId.
        """

        session = requests.Session()

        url = "https://en.wikipedia.org/w/api.php"

        fromrev = None
        torev = None

        if to_id is None:  # compare with parent
            fromrev = self.parent_id
            torev = self.revision_id
        else:  # compare self to to_id, hit getrevision endpoint
            fromrev = self.revision_id
            torev = to_id

        params = {
            #params for Compare API
            #https://www.mediawiki.org/wiki/API:Compare
            'action':"compare",
            'format':"json",
            'fromtitle': self.title,
            'totitle': self.title,
            'fromrev': fromrev,
            'torev': torev
        }

        request = session.get(url=url, params=params)
        data = request.json()

        print(data)
        