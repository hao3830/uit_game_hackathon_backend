from logging import getLogger

from src.utils.db_helper import exec_query, process_join_result

logger = getLogger("app")


class Mission:
    def __init__(
            self,
            _id,
            camera_id,
            img_url,
            mission_score,
            location_desc,
            is_done,
            mission_time
    ):  
        self._id = _id
        self.camera_id = camera_id
        self.img_url = img_url
        self.mission_score = mission_score
        self.is_done = is_done
        self.location_desc=location_desc
        self.mission_time = mission_time
    
    def json(self):
        return {
            "_id": self._id,
            "camera_id": self.camera_id,
            "img_url": self.img_url,
            "mission_score": self.mission_score,
            "is_done": self.is_done,
            "location_desc": self.location_desc,
            "mission_time": self.mission_time
        }

    @staticmethod
    def from_json(_json):
        return Mission(
            _id=_json["_id"],
            camera_id=_json["camera_id"],
            img_url=_json["img_url"],
            mission_score=_json["mission_score"],
            is_done=_json["is_done"], #if _json["is_done"] is not None else 0
            location_desc=_json["location_desc"],
            mission_time=_json["mission_time"]
        )
    
    @staticmethod
    def get_all_pending(
        user_id,
        done=0
    ):
        query = 'SELECT * FROM Mission m WHERE m.is_done="{}" ORDER BY m.mission_time DESC '.format(done)
        # query = "SELECT TOP {} * FROM User".format(top)
        map_list = []
    
        logger.info(f"Query: {query}")

        try:
            _, users = exec_query(query, mode="fetchall")
            if len(map_list):
                users = process_join_result(users, map=map_list)
            return None, list(map(Mission.from_json, users))
        except Exception as err:
            logger.error(f"Cannot exec query: {query}")
            logger.error(err, exc_info=True)
            return "SQLExecuteError", None
    
    @staticmethod
    def insert(Mission):
        query = (
            'INSERT INTO Mission( camera_id, img_url, mission_score, is_done, location_desc) VALUES("{}", "{}", "{}", "{}");'.format(
                Mission.camera_id,
                Mission.img_url,
                Mission.mission_score,
                Mission.is_done,
                Mission.location_desc
            )
        )
        logger.info(f"Query: {query}")

        try:
            exec_query(query)
            return None, Mission
        except Exception as err:
            logger.error(f"Cannot exec query: {query}")
            logger.error(err, exc_info=True)
            return "SQLExecuteError", None

    @staticmethod
    def get_all_mission_by_id(
        mission_id
    ):
        query = 'SELECT * FROM Mission m WHERE m._id="{}";'.format(mission_id)
        # query = "SELECT TOP {} * FROM User".format(top)
        map_list = []
    
        logger.info(f"Query: {query}")

        try:
            _, user = exec_query(query, mode="fetchone")
            if not user:
                return "NotFound", None
            if len(map_list):
                user = process_join_result(user, map=map_list)
            return None,  Mission.from_json(user)
        except Exception as err:
            logger.error(f"Cannot exec query: {query}")
            logger.error(err, exc_info=True)
            return "SQLExecuteError", None
    
    @staticmethod
    def update_status_mission(status, mission_id):
        query = "UPDATE Mission m {}"
        joins = []
        map_list = []
        joins = " ".join(joins)
        query = query.format(joins)
        query += 'SET m.is_done = {}'.format(status)
        query += ' WHERE m.mission_id="{}" ;'.format(mission_id)
        logger.info(f"Query: {query}")
        try:
            _, user = exec_query(query, mode="fetchone")
            if not user:
                return "NotFound", None
            if len(map_list):
                user = process_join_result(user, map=map_list)
            return None, Mission.from_json(user)
        except Exception as err:
            logger.error(f"Cannot exec query: {query}")
            logger.error(err, exc_info=True)
            return "SQLExecuteError", None
    
