from goe.json_client import GoEJsonClient, JsonResult


class MockClient(GoEJsonClient):
    def __init__(self, returns: JsonResult):
        self.returns = returns

    def query(self, *, keys=None) -> JsonResult:
        return self.returns
