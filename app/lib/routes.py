from flask import Blueprint, request, Response, send_file, jsonify
from lib.indigo_renderer import IndigoFactory, IndigoException
from lib.utils import FileHendler
from flask_swagger_ui import get_swaggerui_blueprint
from io import BytesIO
import time

file_hendler = FileHendler(dir='./static/tmp')
swagger_ui_blueprint = get_swaggerui_blueprint(
    base_url="/api/swagger",
    api_url="/static/swagger.json"
)
api = Blueprint('api', __name__)


@api.route('/render', methods=["GET"])
def render_smiles() -> Response:
    smiles = request.args.get("smiles")
    if not smiles:
        return Response("SMILES parameter is required", status=400)
    render_type = 'smiles_render'
    width = int(request.args.get("width", 400))
    height = int(request.args.get("height", 400))
    image_format = request.args.get("format", "svg")
    try:
        service = IndigoFactory.get_renderer(render_type ,width, height, image_format)
        img_bytes = service.render(smiles)
    except IndigoException as e:
        return jsonify({"error": f"Invalid molecule data: {e}"}), 400
    
    file_name = file_hendler.write(img_bytes, image_format)
    file_url = request.host_url.rstrip("/") + f"/static/tmp/{file_name}"
    return jsonify({"url": file_url})


@api.route('/render', methods=["POST"])
def render_molecule() -> Response:
    width = int(request.form.get("width", 400))
    height = int(request.form.get("height", 400))
    image_format = request.form.get("format", "svg").lower()
    smiles = request.form.get("smiles")
    mol_file = request.files.get("mol")
    
    if not smiles and not mol_file:
        return Response("Either 'smiles' or 'mol' file is required", status=400)
    try:
        if smiles:
            service = IndigoFactory.get_renderer("smiles_render", width, height, image_format)
            img_bytes = service.render(smiles)
        else:
            mol_data = mol_file.read()
            service = IndigoFactory.get_renderer("mol_render", width, height, image_format)
            img_bytes = service.render(mol_data)
    except IndigoException as e:
        return jsonify({"error": f"Invalid molecule data: {e}"}), 400
    
    file_name = file_hendler.write(img_bytes, image_format)
    file_url = request.host_url.rstrip("/") + f"/static/tmp/{file_name}"
    return jsonify({"url": file_url})

