from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import GET, DELETE, POST

from vision_project.api.drawing_assembler import DrawingAssembler
from vision_project.api.drawing_model import DrawingModel
from vision_project.drawing.drawing import Drawing


@Resource("/drawing")
class DrawingResource(object):

    @Inject
    def __init__(self, drawing: Drawing, drawing_assembler: DrawingAssembler):
        self.drawing_assembler = drawing_assembler
        self.drawing = drawing

    @GET
    def get_drawing(self) -> DrawingModel:
        return self.drawing_assembler.to_model(self.drawing)

    @POST
    @Path("/clear")
    def clear_drawing(self) -> str:
        self.drawing.clear()
        return "OK"
