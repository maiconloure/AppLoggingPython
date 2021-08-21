from flask import request
from flask_restful import Resource
from app.log_catcher.services.log_catcher import LogCatcherService
import re

class LogCatcher(Resource):
    def __init__(self):
        self.logCatcherService = LogCatcherService()


    def get(self):
        try:
            args = request.args
            subscribers = re.split('[,]+', args['subscribers'])

            if not self.logCatcherService.active:
                if len(subscribers) > 0 and subscribers[0] != '':
                    self.logCatcherService.spamming_streaming(subscribers)
            else:
                return {'message': "LogCatcher already running"}, 200

            return {'message': "LogCatcher started successfully"}, 200

            
        except Exception as error:
            return {'error': str(error)}, 500
