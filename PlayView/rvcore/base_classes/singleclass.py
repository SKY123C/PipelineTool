from PySide6 import QtCore


class SignalClass(type(QtCore.QObject)):
    instance = None
    def __init__(self, name, bases, dict):

        super(SignalClass, self).__init__(name, bases, dict)

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance


