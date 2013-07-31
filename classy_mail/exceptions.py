
# Exceptions

class ImpossibleEmail(Exception):
    pass


class NoFromAddress(ImpossibleEmail):
    pass


class NoToAddress(ImpossibleEmail):
    pass


class NoSubject(ImpossibleEmail):
    pass


class NoBody(ImpossibleEmail):
    pass

