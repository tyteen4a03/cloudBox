# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import logging

from jinja2 import Environment, FileSystemLoader
from tornado import web

from cloudbox.common.mixins import CloudBoxFactoryMixin
from cloudbox.web.webhandlers import index


class WebServerApplication(web.Application, CloudBoxFactoryMixin):
    """
    I am the WebServer application.
    """

    def __init__(self, parentService):
        self.parentService = parentService
        self.settings = None
        self.handlers = [
            (r"/", index.IndexRequestHandler)
        ]
        self.logger = logging.getLogger("cloudbox.web")
        self.templater = Environment(loader=FileSystemLoader("./web/templates"))
        web.Application.__init__(self, self.handlers, **self.parentService.settings["web"]["web-server-settings"])

    def log_request(self, handler):
        if handler.get_status() < 400:
            logMethod = self.logger.debug
        elif handler.get_status() < 500:
            logMethod = self.logger.warning
        else:
            logMethod = self.logger.error
        request_time = 1000.0 * handler.request.request_time()
        logMethod("%d %s %.2fms" % (handler.get_status(), handler._request_summary(), request_time))