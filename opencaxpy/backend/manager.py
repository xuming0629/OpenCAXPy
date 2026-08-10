from .numpy_backend import NumPyBackend
class BackendManager:
    def __init__(self):
        self._backends = {"numpy": NumPyBackend()}
        self._name = "numpy"
    def set_backend(self, name):
        if name not in self._backends: raise KeyError(name)
        self._name = name
    @property
    def current(self): return self._backends[self._name]
    @property
    def name(self): return self._name
    def __getattr__(self, name): return getattr(self.current, name)
backend_manager = BackendManager()
