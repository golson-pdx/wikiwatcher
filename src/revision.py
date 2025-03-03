'''defines revision base class'''
from datetime import datetime
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
    def __init__(self) -> None:
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

    def get_contents(self): #start and end time stamps???
        ''' Returns the content of the page at this revision'''

        session = requests.Session()

        url = "https://www.wikipedia.org/w/api.php"

        params = {
            "action": "parse",
            "format": "json",
            "oldid": self.revision_id,
            "prop": "text|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks",
            "formatversion": "2"
        }
        try:
            request = session.get(url=url, params=params)
        except Exception as exc:
            raise SystemExit("Revision ID missing") from exc
        data = request.json()
        print(data)

    def check_to_id(self, to_id):
        '''returns fromrev and torev args to parameters in get_diff'''
        if to_id is None:
            return self.revision_id, self.parent_id
        return self.revision_id, to_id

    def get_diff(self, to_id: int = None):
        """ Returns the difference between this revision and its parent 
        in this revision's article's history, unless a toId is specified in
        which case this revision is compared with toId.
        """
        session = requests.Session()

        url = "https://en.wikipedia.org/w/api.php"

        fromrev, torev = self.check_to_id(to_id)

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
        