from jinja2 import Markup
from datetime import datetime

class momentjs:

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")

    def proper(self):
        delta = datetime.utcnow() - self.timestamp 
        if delta.seconds > 21600:
            return self.calendar()
        else:
            return self.fromNow()
