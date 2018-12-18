from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import GET, DELETE, POST, OPTIONS
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.request.response import Response

from vision_project.api.drawing_assembler import DrawingAssembler
from vision_project.api.drawing_model import DrawingModel, LineModel
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

    @POST
    def add_line(self, line: LineModel) -> str:
        self.drawing.draw_line(*self.drawing_assembler.from_line_model(line))
        return "OK"

    @OPTIONS
    def preflight(self):
        headers = Headers()
        headers['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS, DELETE"
        headers['Access-Control-Allow-Headers'] = '*'
        return Response(200, headers, "")
