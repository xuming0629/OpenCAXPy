from opencaxpy import MeshRefiner, refinement_registry


class DummyRefiner(MeshRefiner):
    method = "dummy"
    supported_cell_types = ("triangle3",)

    def refine_once(self, mesh, context):
        raise RuntimeError("not executed")


def test_external_refiner_registration():
    refinement_registry.register(DummyRefiner(), replace=True)
    assert "dummy" in refinement_registry.methods("triangle3")
