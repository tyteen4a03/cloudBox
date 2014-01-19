# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from tornado.web import RequestHandler


class BaseRequestHandler(RequestHandler):
    @property
    def db(self):
        return self.application.parentService.db

    @property
    def templater(self):
        return self.application.templater