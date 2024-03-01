class ImageCacheManager:
    
    def __init__(self) -> None:
        self.__cache_map = {}
        ...
    
    def register_cache(self, table, delegate):
        cache_item = CacheItem(table)
        self.__cache_map[delegate] = cache_item
        ...
    
    def unregister_cache(self, table):
        if table in self.__cache_map:
            self.__cache_map.pop(table)
        ...




class CacheItem:
    
    def __init__(self, table) -> None:
        pass
        self.table = table
        self.__image_cahce_list = []
    
    def start_cache(self):
        
        
        ...