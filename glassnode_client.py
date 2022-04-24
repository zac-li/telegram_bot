import requests
import iso8601
from iso8601 import ParseError
import pandas as pd


class GlassnodeClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def get(self, url, a="BTC", i="24h", c="native", s=None, u=None, in_df=False):
        p = dict()
        p["a"] = a
        p["i"] = i
        p["c"] = c

        if s is not None:
            try:
                p["s"] = iso8601.parse_date(s).strftime("%s")
            except ParseError:
                p["s"] = s

        if u is not None:
            try:
                p["u"] = iso8601.parse_date(u).strftime("%s")
            except ParseError:
                p["u"] = s

        p["api_key"] = self.api_key

        r = requests.get(url, params=p)

        try:
            r.raise_for_status()
        except Exception as e:
            print(e)
            print(r.text)

        if not in_df:
            return r.json()

        try:
            df = pd.read_json(r.text, convert_dates=["t"])
            return df
        except Exception as e:
            print(e)
