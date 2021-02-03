

class PropostalServiceError(Exception):
    def __init__(self, request_code):
        self.message = f"Invalid request. Error code {request_code}"
        super().__init__()

    def __str__(self):
        return self.message


class DecodeJsonError(Exception):
    def __init__(self, class_name, method_name):
        self.message = f"Can`t decode a json in {class_name}.{method_name}"
        super().__init__()

    def __str__(self):
        return self.message