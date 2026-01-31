from indigo import Indigo, IndigoException
from indigo.renderer import IndigoRenderer

class IndigoRendererService:
    def __init__(self, width: int, height: int, image_format: str):
        self.indigo = Indigo()
        self.renderer = IndigoRenderer(self.indigo)
        self.indigo.setOption("render-margins", 10, 10)
        self.indigo.setOption("render-image-size", width, height)
        self.indigo.setOption("render-output-format", image_format)
        self.indigo.setOption("render-background-color", "255, 255, 255")


class RenderFromSmiles(IndigoRendererService):
    def render(self, smiles: str) -> bytes:
        mol = self.indigo.loadMolecule(smiles)
        return self.renderer.renderToBuffer(obj=mol)


class RenderFromMol(IndigoRendererService):
    def render(self, data: bytes) -> bytes:
        mol = self.indigo.loadMoleculeFromBuffer(data)
        return self.renderer.renderToBuffer(obj=mol)


class IndigoFactory:
    @staticmethod
    def get_renderer(type_of_render: str, width=400, height=400, image_format="svg") -> IndigoRendererService:
        if type_of_render == "smiles_render":
            return RenderFromSmiles(width, height, image_format)
        elif type_of_render == "mol_render":
            return RenderFromMol(width, height, image_format)
        else:
            raise ValueError(f"Unknown renderer type: {type_of_render}")
        