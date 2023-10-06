"""Define custom exceptions."""


class YaoyaError(Exception):
    pass


class AuthenticationError(YaoyaError):
    pass


class NotFoundError(YaoyaError):
    def __init__(self, entity_id: str) -> None:
        self.entity_id = entity_id
