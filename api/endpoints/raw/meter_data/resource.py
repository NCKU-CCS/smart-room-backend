from datetime import datetime, timezone
from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from loguru import logger

from config import SESSION, NORMAL_VOLTAGE, VOLTAGE, TZ
from utils.oauth import g, USER_AUTH
from database.migrations.models import MeterData


class RawMeterDataResource(Resource):
    """Get Raw Meter Data"""

    def __init__(self):
        # Get Period of Meter data
        self._set_get_parser()

    def _set_get_parser(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument("sensor", type=str, required=True, location="values")
        self.get_parser.add_argument("start", type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'), required=True, location="values")
        self.get_parser.add_argument("end", type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'), required=True, location="values")

    # pylint: disable=R0201
    @USER_AUTH.login_required
    def get(self):
        """Get Latest Sensor Data"""
        args = self.get_parser.parse_args()
        logger.info(f"[GET Raw Meter Data Request]\n User: {g.account}, Meter: {args['sensor']}, Start: {args['start']}, End: {args['end']}")
        data = SESSION.query(MeterData).filter(
            MeterData.sensor == args['sensor'],
            MeterData.created.between(args['start'], args['end']
        )).order_by(MeterData.created).all()

        if "WATER_DISPENSER" in args['sensor']:
            voltage = NORMAL_VOLTAGE
        else:
            voltage = VOLTAGE

        
        result = [{
            "created": (d.created.replace(tzinfo=timezone.utc).astimezone(tz=TZ)).strftime('%Y-%m-%dT%H:%M:%S'),
            "power": d.current * voltage,
        } for d in data]
        return make_response(jsonify(result), 200)

    # pylint: enable=R0201
