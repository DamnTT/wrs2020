#!/usr/bin/python
import re
import json
import requests

MAP_NAME = "HOME_AREA"

class Request(object):
    def __init__(self, method, path):
        self.method = method.upper()
        self.path = path
        self.h = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept-Language": "en-US",
            "Authorization": "Basic ZGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA=="
        }

    def __call__(self, f):
        def wrapper(obj, *args, **kwargs):
            payload = f(obj, *args, **kwargs)
            URL = "{}{}".format(obj.host, self.path)

            if payload is not None:
                if payload.has_key("PATH"):
                    URL = "{}{}".format(URL, payload.get("PATH"))
                try:
                    res = requests.request(self.method,
                                           url=URL,
                                           headers=self.h,
                                           data=json.dumps(payload),
                                           timeout=3)
                except requests.RequestException as e:
                    print(e)
                    return
            else:
                try:
                    res = requests.request(self.method,
                                           url=URL,
                                           headers=self.h,
                                           timeout=3)
                except requests.RequestException as e:
                    print(e)
                    return
            return res
        return wrapper


class MIR(object):
    def __init__(self, host):
        if not "http" in host:
            print("WARRING: Maybe the host name is error.")

        self.host = host

    @Request(method="get", path="/status")
    def get_status(self):
        pass

    @Request(method="put", path="/status")
    def status(self, set_state):
        STATE = {"Ready": 3, "Pause": 4}

        # Check whether input 'set_state' is correct
        if isinstance(set_state, (str, int)):
            if isinstance(set_state, str):
                s = STATE.get(set_state, 4)
        else:
            print("ERROR type of set_state")
            return

        body = {
            "state_id": s
        }
        return body

    @Request(method="get", path="/system/info")
    def system_info(self):
        pass

    @Request(method="get", path="/missions")
    def get_missions(self):
        pass

    def get_mission_guid(self, mission):
        r = self.get_missions()
        rjson = json.loads(r.text)
        for l in rjson:
            if l.get("name") == mission:
                return l.get("guid")
        print("No this mission")
        #print(r.text)
        return None

    @Request(method="get", path="/mission_queue")
    def get_mission_queue(self):
        pass

    @Request(method="post", path="/mission_queue")
    def mission_queue(self, mission):
        body = {
            "mission_id": mission
        }
        return body

    @Request(method="delete", path="/mission_queue")
    def clear_mission_queue(self):
        pass

    @Request(method="get", path="/positions")
    def get_positions(self):
        pass

    @Request(method="get", path="/positions")
    def get_position_by_id(self, guid):
        return {"PATH": "/" + guid}

    def get_position_guid(self, position_name):
        r = self.get_positions()
        rjson = json.loads(r.text)
        for l in rjson:
            if l.get("name") == position_name:
                return l.get("guid")
        print("No this position")
        return None

    @Request(method="post", path="/positions")
    def add_position(self, name, x, y, yaw, position_type=0):
        map_guid = self.get_map_guid(MAP_NAME)
        body = {
            "map_id": map_guid,
            "name": name,
            "orientation": yaw,
            "pos_x": x,
            "pos_y": y,
            "type_id": position_type
        }
        return body

    @Request(method="get", path="/maps")
    def get_maps(self):
        pass

    def get_map_guid(self, map_name):
        r = self.get_maps()
        rjson = json.loads(r.text)
        for l in rjson:
            if l.get("name") == map_name:
                return l.get("guid")
        print("No this position")
        return None

    ## TODO: Understand action to achieve related move?
    # Use post /missions to add new mission
    # Use post /missions/{mission_id}/actions to add new action
    # Use put /missions/{mission_id}/actions/{guid} to modify value of action
    # Use put /mission/{guid} to modify value of mission
    ##TODO: Clear ERROR Code
