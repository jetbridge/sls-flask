"""Monitoring endpoints."""
from flask_smorest import Blueprint
from flask.views import MethodView
from marshmallow import fields as f, Schema
from TEMPLATE.db import db

blp = Blueprint("Monitoring", __name__, url_prefix="/api/monitoring")


class MonitoringSchema(Schema):
    ok = f.Boolean(dump_only=True)


@blp.route("")
class Monitoring(MethodView):
    @blp.response(MonitoringSchema())
    def get(self):
        """Check if site and DB are up."""
        return {"ok": bool(db.engine.execute("SELECT 1").scalar())}
