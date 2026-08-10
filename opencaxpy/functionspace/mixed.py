class MixedSpace:
    def __init__(self,*spaces): self.spaces=tuple(spaces)
    @property
    def number_of_global_dofs(self):
        return sum(s.number_of_global_dofs for s in self.spaces)
