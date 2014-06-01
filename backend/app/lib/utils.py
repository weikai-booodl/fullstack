from datetime import datetime
from flask import request


def today():
    return datetime.utcnow().date()


class Paginator(object):
    """
    notice limit=-1 means no limit
    """
    @property
    def offset(self):
        return int(request.args.get("offset", 0))

    @property
    def limit(self):
        return int(request.args.get("limit", 20))

    def get_pagination_hint(self, rows_in_page):
        hint = {}
        if self.offset > 0:
            offset = 0 if self.limit==-1 else max(0, self.offset-self.limit)
            hint["prev_page"] = dict(url="%s?offset=%d&limit=%d" % (request.base_url,offset,self.limit),
                                         offset=offset,
                                         limit=self.limit)

        if self.limit == len(rows_in_page):
            offset = self.limit + self.offset
            hint["next_page"] = dict(url="%s?offset=%d&limit=%d" % (request.base_url, offset, self.limit),
                                        offset=offset,
                                        limit=self.limit)

        return hint

