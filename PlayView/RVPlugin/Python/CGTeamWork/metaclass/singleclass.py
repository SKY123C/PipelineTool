from PySide2 import QtCore


class SignalClass(type(QtCore.QObject)):

    def __init__(self, name, bases, dict):

        super(SignalClass, self).__init__(name, bases, dict)

    def __call__(self, *args, **kwargs):

        if self.obj:
            return self.obj
        else:
            obj = super(SignalClass,self).__call__(*args, **kwargs)
            self.obj = obj
            return obj
        



