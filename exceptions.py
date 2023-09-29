class TelegramMessageError(Exception):
    """Error when sending a message in a Telegram."""
    pass


class WSSessionPublicError(Exception):
    """Error related to a public WebSocket session."""
    pass


class WSSessionPrivateError(Exception):
    """Error related to a private WebSocket session."""
    pass


class HTTPSessionError(Exception):
    """Error related to an HTTP WebSocket session."""
    pass
