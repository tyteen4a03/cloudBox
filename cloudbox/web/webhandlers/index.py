# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.web.webhandlers.base import BaseRequestHandler


class IndexRequestHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        self.write(self.templater.get_template("index.html").render())

    post = get