from flask_restful import Resource, reqparse, Api
from flask import Flask, json, jsonify, request, make_response
from werkzeug.exceptions import HTTPException
from .database import db
from application.models import User, Tracker, TrackerLog
from application.utilities import *


# API VALIDATIONS...

class InternalServerError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('Internal Server Error', status_code)

class NotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('Object Not Found', status_code)

class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code":error_code, "error_message":error_message}
        self.response = make_response(json.dumps(message), status_code)


create_tracker_parser = reqparse.RequestParser()
create_tracker_parser.add_argument('user_id')
create_tracker_parser.add_argument('tracker_name')
create_tracker_parser.add_argument('description')
create_tracker_parser.add_argument('track_type')
create_tracker_parser.add_argument('settings')

update_tracker_parser = reqparse.RequestParser()
update_tracker_parser.add_argument('tracker_name')
update_tracker_parser.add_argument('description')
update_tracker_parser.add_argument('settings')


#all the apis extends the resource class

class UserAPI(Resource):
    def get(self, username):
        print("getting username", username)

        if not usernamevalidation(username):
            raise BusinessValidationError(status_code=400, error_code="USER01", error_message="Invalid username, simple string without spaces expected")

        try:
            userobj = User.query.filter_by(username=username).first()
        except:
            raise InternalServerError(status_code=500)
        print(userobj)  #####
        if userobj:
            # v = {"user_id":userobj.user_id,"username":username,"fname":userobj.fname,"lname":userobj.lname,"password":(userobj.password).decode('UTF-8')}
            v = {"user_id":userobj.user_id,"username":username,"fname":userobj.fname,"lname":userobj.lname,"password":userobj.password}

            print(v)
            return v
        else:
            raise NotFoundError(status_code=404)


class AllTrackersAPI(Resource):
    def get(self, user_id):
        print(user_id)
        if not idvalidation(user_id):
            raise BusinessValidationError(status_code=400, error_code="TRACKER05", error_message="Invalid user_id/tracker_id, just integer expected")
        
        try:
            alltrackers = Tracker.query.filter_by(user_id=user_id).all()
        except:
            raise InternalServerError(status_code=500)
        
        recordList = []
        for newtracker in alltrackers:
            t_id = newtracker.tracker_id
            t_name = newtracker.tracker_name
            lastlog = TrackerLog.query.filter_by(tracker_id=t_id,user_id=user_id).order_by(TrackerLog.timestamp.desc()).limit(1).first()
            # print(type(lastlog), lastlog.timestamp)
            # lastlog = TrackerLog.query.filter_by(tracker_id=t_id,user_id=user_id).order_by(TrackerLog.timestamp.desc()).limit(1).one()
            newrec = {}
            # recordList.append(newrec)
            newrec["tracker_id"] = t_id
            newrec["tracker_name"] = t_name
            if lastlog:
                newrec["lastlog"] = lastlog.timestamp
            else: #if lastlog is None, i.e, no log recorded yet
                newrec["lastlog"] = lastlog
            recordList.append(newrec)
        return recordList


class TrackerAPI(Resource):
    def get(self, tracker_id):
        print("getting ID's", tracker_id)
        if not idvalidation(tracker_id):
            raise BusinessValidationError(status_code=400, error_code="TRACKER05", error_message="Invalid user_id/tracker_id, just integer expected")

        try:
            trackerobj = Tracker.query.get(tracker_id)
        except:
            raise InternalServerError(status_code=500)

        if trackerobj:
            v = {
            "user_id": trackerobj.user_id,
            "tracker_id": tracker_id,
            "tracker_name": trackerobj.tracker_name,
            "description": trackerobj.description,
            "track_type": trackerobj.track_type,
            "settings": trackerobj.settings
            }
            return v
        else:
            raise NotFoundError(status_code=404)

    def put(self, tracker_id):
        print("Updating Tracker", tracker_id)
        args = update_tracker_parser.parse_args()
        # user_id = args.get("user_id", None)
        tracker_name = args.get("tracker_name", None)
        description = args.get("description", None)
        # track_type = args.get("track_type", None)
        settings = args.get("settings", None)

        if not idvalidation(tracker_id):
            raise BusinessValidationError(status_code=400, error_code="TRACKER05", error_message="Invalid user_id/tracker_id, just integer expected")
        else:
            tracker_id = int(tracker_id)
        
        # if not normalvalidation(tracker_name):
        if (tracker_name is None) or (not normalvalidation(tracker_name)):
            raise BusinessValidationError(status_code=400, error_code="TRACKER01", error_message="Invalid Tracker Name, simple string expected.")
        if (description is None) or (not normalvalidation(description)):
            raise BusinessValidationError(status_code=400, error_code="TRACKER02", error_message="Invalid description, simple string expected.")
        
        try:
            updatetracker = Tracker.query.get(tracker_id)
        except:
            raise InternalServerError(status_code=500)
        if updatetracker is None:
            raise NotFoundError(status_code=404)
        track_type = updatetracker.track_type
        if (track_type=='Multiple_Choice') and ((settings is None) or (not csvvalidation(settings))):
            raise BusinessValidationError(status_code=400, error_code="TRACKER04", error_message="Invalid settings, csv values without spaces expected.")

        
        if track_type=='Numerical':
            updatetracker.tracker_name = tracker_name
            updatetracker.description = description
            # newtracker = Tracker(user_id=user_id, tracker_name=tracker_name, description=description, track_type=track_type)
        elif track_type=='Multiple_Choice':
            updatetracker.tracker_name = tracker_name
            updatetracker.description = description
            updatetracker.settings = settings
            # newtracker = Tracker(user_id=user_id, tracker_name=tracker_name, description=description, track_type=track_type, settings=settings)
        db.session.commit()
        v = {
            "user_id": updatetracker.user_id,
            "tracker_id": tracker_id,
            "tracker_name": updatetracker.tracker_name,
            "description": updatetracker.description,
            "track_type": updatetracker.track_type,
            "settings": updatetracker.settings
            }
        print("value of v===========",v)
        return v, 200
        
    def delete(self, tracker_id):
        print("Deleting Tracker", tracker_id)
        if not idvalidation(tracker_id):
            raise BusinessValidationError(status_code=400, error_code="TRACKER05", error_message="Invalid user_id/tracker_id, just integer expected")
        else:
            tracker_id = int(tracker_id)

        try:
            deletetracker = Tracker.query.get(tracker_id)
        except:
            raise InternalServerError(status_code=500)
        if deletetracker is None:
            raise NotFoundError(status_code=404)
        
        delrecs = TrackerLog.query.filter_by(tracker_id=tracker_id).all()
        #delete all the enrollments
        if delrecs:
            for rec in delrecs:
                db.session.delete(rec)
        db.session.commit()

        db.session.delete(deletetracker)
        db.session.commit()
        # delrecs = TrackerLog.query.filter_by(tracker_id=tracker_id).all()
        # #delete all the enrollments
        # if delrecs:
        #     for rec in delrecs:
        #         db.session.delete(rec)
        # db.session.commit()
        return '', 200

    def post(self):
        print("creating new tracker")
        args = create_tracker_parser.parse_args()
        user_id = args.get("user_id", None)
        tracker_name = args.get("tracker_name", None)
        description = args.get("description", None)
        track_type = args.get("track_type", None)
        settings = args.get("settings", None)

        if not idvalidation(user_id):
            print("IDVALIDATION FAILED")
            raise BusinessValidationError(status_code=400, error_code="TRACKER05", error_message="Invalid user_id/tracker_id, just integer expected")
        else:
            user_id = int(user_id)

        # if (user_id is None) or (not isinstance(user_id, int)):
        #     raise BusinessValidationError(status_code=400, error_code="TRACKER05", error_message="Invalid user_id, integer expected")
        if (tracker_name is None) or (not normalvalidation(tracker_name)):
            print("TRACKER_NAME VALIDATION FAILED")
            raise BusinessValidationError(status_code=400, error_code="TRACKER01", error_message="Invalid Tracker Name, simple string expected.")
        if (description is None) or (not normalvalidation(description)):
            print("DESCRIPTION VALIDATION FAILED")
            raise BusinessValidationError(status_code=400, error_code="TRACKER02", error_message="Invalid description, simple string expected.")
        if (track_type is None) or (track_type not in ['Numerical', 'Multiple_Choice']):
            print("TRACK_TYPE VALIDATION FAILED")
            raise BusinessValidationError(status_code=400, error_code="TRACKER03", error_message="Invalid track_type, accepts only two values - 'Numerical' or 'Multiple_Choice'.")
        if (track_type=='Multiple_Choice') and ((settings is None) or (not csvvalidation(settings))):
            print("SETTINGS OR CSV VALIDATION FAILED")
            raise BusinessValidationError(status_code=400, error_code="TRACKER02", error_message="Invalid settings, csv values without spaces expected.")
        
        userexist = User.query.get(user_id)
        if userexist is None:
            print("USER DOESNOT EXIST")
            raise NotFoundError(status_code=409)
            # raise BusinessValidationError(status_code=400, error_code="TRACKER05", error_message="Invalid user_id, user does not exist")

        if track_type=='Numerical':
            newtracker = Tracker(user_id=user_id, tracker_name=tracker_name, description=description, track_type=track_type)
        elif track_type=='Multiple_Choice':
            newtracker = Tracker(user_id=user_id, tracker_name=tracker_name, description=description, track_type=track_type, settings=settings)
        db.session.add(newtracker)
        db.session.commit()
        return '', 201

