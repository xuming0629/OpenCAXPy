class BilinearForm:
    def __init__(self, space):
        self.space=space; self.integrators=[]
    def add_integrator(self, integ):
        self.integrators.append(integ); return self
