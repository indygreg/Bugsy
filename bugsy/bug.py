import requests


VALID_STATUS = ["RESOLVED", "ASSIGNED", "NEW", "UNCONFIRMED"]
VALID_RESOLUTION = ["FIXED", "INCOMPLETE", "INVALID", "WORKSFORME", "DUPLICATE", "WONTFIX"]


class BugException(Exception):
    """
        If we try do something that is not allowed to a bug then
        this error is raised
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Message: %s" % self.msg


class Bug(object):
    """This represents a Bugzilla Bug"""

    _bug = {'id':None}

    def __init__(self, bugzilla_url=None, token=None, **kwargs):
        """
            Defaults are set if there are no kwargs passed in. To pass in
            a dict create the Bug object like the following

            :param bugzilla_url: This is the Bugzilla REST URL endpoint. Defaults to None
            :param token: Login token generated when instantiating a Bugsy() object with
                          a valid username and password

            >>> bug = Bug(**myDict)
        """
        self.bugzilla_url = bugzilla_url
        self.token = token
        self._bug = dict(**kwargs)

    def id():
        doc = """
            Property for getting the ID of a bug.

            >>> bug.id
            123456
        """
        def fget(self):
            return self._bug.get('id', None)
        return locals()
    id = property(**id())

    def summary():
        doc = """
            Property for getting and setting the bug summary

            >>> bug.summary = "I like cheese"
            >>> bug.summary
            "I like cheese"
        """
        def fget(self):
            return self._bug.get('summary', '')
        def fset(self, value):
            self._bug['summary'] = value
        def fdel(self):
            del self._bug['summary']
        return locals()
    summary = property(**summary())

    def status():
        doc = """
            Property for getting or setting the bug status

            >>> bug.status = "REOPENED"
            >>> bug.status
            "REOPENED"
        """
        def fget(self):
            return self._bug.get('status', '')
        def fset(self, value):
            if self._bug.get('id', None):
                if value in VALID_STATUS:
                    self._bug['status'] = value
                else:
                    raise BugException("Invalid status type was used")
            else:
                raise BugException("Can not set status unless there is a bug id. Please call Update() or before setting")
        def fdel(self):
            del self._bug['status']
        return locals()
    status = property(**status())

    def resolution():
        doc = """
            Property for getting or setting the bug resolution

            >>> bug.resolution = "FIXED"
            >>> bug.resolution
            "FIXED"
        """
        def fget(self):
            return self._bug['resolution']
        def fset(self, value):
            if value in VALID_RESOLUTION:
                self._bug['resolution'] = value
            else:
                raise BugException("Invalid resolution type was used")
        def fdel(self):
            del self._bug['resolution']
        return locals()
    resolution = property(**resolution())

    def to_dict(self):
        """
            Return the raw dict that is used inside this object
        """
        return self._bug

    def update(self):
        """
            Update this object with the latest changes from Bugzilla

            >>> bug.status
            'NEW'
            #Changes happen on Bugzilla
            >>> bug.update()
            >>> bug.status
            'FIXED'
        """
        if self._bug.has_key('id'):
            result = requests.get(self.bugzilla_url + "/bug/%s" % self._bug['id']).json()
            self._bug = dict(**result['bugs'][0])
        else:
            raise BugException("Unable to update bug that isn't in Bugzilla")
