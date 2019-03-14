from flask_rest_api import Blueprint
from flask.views import MethodView
from marshmallow import fields as f, Schema
from TEMPLATE.api import api
from TEMPLATE.database import db


blp = Blueprint(
    'monitoring', __name__,
    url_prefix='/api',
    description='Site Monitoring'
)


@api.definition('Monitoring')
class MonitoringSchema(Schema):
    class Meta:
        strict = True

    ok = f.Boolean(dump_only=True)


@blp.route('/monitoring')
class Monitorings(MethodView):

    @blp.response(MonitoringSchema())
    def get(self):
        """Check if site and DB are up."""
        return {'ok': bool(db.engine.execute("SELECT 1").scalar())}
