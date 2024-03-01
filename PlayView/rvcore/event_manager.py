from rvcore.base_classes import base_manager
from rvcore.rv_system import base_event



class EventData:

    def __init__(self) -> None:
        self.__event_data = {}

    @property
    def data(self):
        return self.__event_data

    @data.setter
    def data(self, event_dict:dict, **kargs):
        if event_dict:
            for event_name, event_info in event_dict.items():
                if event_name in self.__event_data:
                    print("warning")
            self.__event_data.update(event_dict)


    def add_func(self, event_name, func, *args):
        event = self.__event_data.get(event_name).get("obj")
        if not event:
            return
        event.add_func(func, *args)


class EventManager(base_manager.Manager):

    def __init__(self) -> None:
        super().__init__()
        self.event_data = EventData()
        self.register_init()

    def register_init(self):
        for event_class in base_event.RVEvent.__subclasses__():
            event_obj = event_class()
            self.event_data.data = {event_obj.event_name:{"obj":event_obj}}
    
    def add_callback(self, event_name, func, *args):
        if not hasattr(func, "__call__"):
            return
        self.event_data.add_func(event_name, func, *args)
    
    def __getitem__(self, key):
        if self.event_data.data.get(key):
            return self.event_data.data[key].get("obj").rv_event
    
    def register_event(self, event_name, **kargs):
        if event_name:
            event = type(event_name, (base_event.RVEvent,), {})
            self.event_data.data = {event_name:{"obj":event()}}




