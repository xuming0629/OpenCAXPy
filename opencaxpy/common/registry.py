class Registry:
    def __init__(self, name):
        self.name = name
        self._items = {}
    def register(self, key, item=None):
        key = key.lower()
        def deco(obj):
            if key in self._items:
                raise KeyError(f"{key!r} already registered in {self.name}")
            self._items[key] = obj
            return obj
        return deco(item) if item is not None else deco
    def get(self, key):
        return self._items[key.lower()]
    def keys(self):
        return tuple(self._items)
