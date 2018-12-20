from jivago.lang.annotations import Inject, Serializable
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import GET, DELETE, POST, OPTIONS
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.request.response import Response

from vision_project.api.drawing_assembler import DrawingAssembler
from vision_project.api.drawing_model import DrawingModel, LineModel, TextModel
from vision_project.api.text_assembler import TextAssembler
from vision_project.drawing.drawing import Drawing


@Resource("/drawing")
class DrawingResource(object):

    @Inject
    def __init__(self, drawing: Drawing, drawing_assembler: DrawingAssembler, text_assembler: TextAssembler):
        self.drawing_assembler = drawing_assembler
        self.drawing = drawing
        self.text_assembler = text_assembler

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

    @POST
    @Path("/text")
    def add_text(self, text: TextModel) -> str:
        self.drawing.add_text(*self.text_assembler.from_text_model(text))
        return "OK"

    @OPTIONS
    @Path("/text")
    def preflightAgain(self):
        return self.preflight()

    @OPTIONS
    def preflight(self):
        headers = Headers()
        headers['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS, DELETE"
        headers['Access-Control-Allow-Headers'] = '*'
        return Response(200, headers, "")

    @POST
    @Path("/lock")
    def lock(self) -> str:
        self.drawing.lock()
        return ""

    @POST
    @Path("/unlock")
    def unlock(self) -> str:
        self.drawing.unlock()
        return ""

    @OPTIONS
    @Path("/lock")
    def lock_preflight(self) -> Response:
        return self.preflight()

    @OPTIONS
    @Path("/unlock")
    def unlock_preflight(self) -> Response:
        return self.preflight()

    @GET
    @Path("/lock")
    def is_locked(self) -> dict:
        return {"locked": self.drawing.locked}
