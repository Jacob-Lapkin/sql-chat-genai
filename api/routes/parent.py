from flask import Blueprint
from .insights import insights_bp

parent_bp = Blueprint('parent_bp', __name__)

parent_bp.register_blueprint(insights_bp)