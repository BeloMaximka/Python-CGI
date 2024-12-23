class RestModel:
    def __init__(self, status=200, meta={}, data:any=None):
        self.status = status if isinstance(status, RestStatus) else RestStatus(status)
        self.meta = meta
        self.data = data

    def to_dict(self):
        return {
            "status": self.status.to_dict(),
            "meta": self.meta.to_dict() if isinstance(self.meta, RestMeta) else self.meta,
            "data": self.data
        }

class RestStatus:
    def __init__(self, status_code:int, reason_phrase:str=None, is_success:bool|None=None):
        self.statusCode = status_code
        self.reasonPhrase = reason_phrase if reason_phrase is not None else self.phrase_by_code(status_code)
        self.isSuccess = is_success if is_success is not None else status_code < 400

    def phrase_by_code(self, status_code:int) -> str:
        match status_code:
            case 200: return "OK"
            case 405: return "Method Not Allowed"
            case 415: return "Unsupported Media Type"
            case _: return ""

    def to_dict(self):
        return {
            "statusCode": self.statusCode,
            "reasonPhrase": self.reasonPhrase,
            "isSuccess": self.isSuccess
        }

class RestMeta:
    def __init__(self, meta):
        self.meta = meta

    def to_dict(self):
        return self.meta