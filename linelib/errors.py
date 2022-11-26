class InvalidSignature(Exception):
    """
    Represents an invalid signature that was sent by an unregistered application / request.
    """
    pass

class AlreadyHandled(Exception):
    """
    It has already been handled.
    """
    pass

class CommandNotFound(Exception):
    """
    Command was not registered.
    """
    pass

class CalculationNotReady(Exception):
    """
    The calculation was not completed.
    """
    pass

class OutOfService(Exception):
    """
    Out of service scope.
    """
    pass

class Unsupported(Exception):
    """
    Unsupported method / function.
    """
    pass

class LineAPI(Exception):
    """
    LINE API response that contains errors.
    """
    pass

def lineApiError(req: dict) -> None:
    if "message" in req:
        err = []
        for i in req["details"]:
            err.append("• " + i["property"] + ": " + i["message"])
        raise LineAPI("\n\n" + "\n".join(err))
