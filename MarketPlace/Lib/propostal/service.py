import requests, json

class PropostalService(object):
    def __init__(self):
        self.response = object()
        self.text = None

    def __iter__(self):
        return iter(self.text)

    def __getitem__(self, key: str):
        return self.text[key]

    def request(self, raise_exception: bool, body: dict) -> object:
        self.response = requests.post('https://b5c49244-9620-485d-9b32-806899842a22.mock.pstmn.io/proposal', json=body)
        if raise_exception and self.response.status_code >= 300:
            raise PropostalServiceError(request_code=self.response.status_code)
        return self

    def decode_to_json(self) -> object:
        try:
            self.text = json.loads(self.response.text)
        except Exception:
            raise DecodeJsonError(class_name=self.__class__.__name__, method_name=self.decode_to_json.__name__)
        return self