from enum import StrEnum


class ServerEvent(StrEnum):
    ON_AUTH = 'on_auth'
    ON_CLOSE = 'on_close'
    ON_INIT = 'on_init'
    ON_QUERY = 'on_query'
    ON_STORE = 'on_store'
