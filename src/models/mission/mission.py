from logging import getLogger

from src.utils.db_helper import exec_query, process_join_result

logger = getLogger("app")


class Mission:
    def __init__(
            self,
            camera_id,
            img_url,
            mission_score,
            is_done
    ):
        self.camera_id = camera_id
        self.img_url = img_url
        self.mission_score = mission_score
        self.is_done = is_done
    
    def json(self):
        return {
            "camera_id": self.camera_id,
            "img_url": self.img_url,
            "mission_score": self.mission_score,
            "is_done": self.is_done
        }

    @staticmethod
    def from_json(_json):
        return Mission(
            camera_id=_json["camera_id"],
            img_url=_json["img_url"],
            mission_score=_json["mission_score"],
            is_done=_json["is_done"] #if _json["is_done"] is not None else 0
        )
    
    @staticmethod
    def get_all_pending(
        done=0
    ):
        query = "SELECT * FROM Mission m WHERE m.is_done={} ORDER BY m.mission_time DESC ".format(done)
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
            'INSERT INTO Mission( camera_id, img_url, mission_score,is_done) VALUES("{}", "{}", "{}", "{}");'.format(
                Mission.camera_id,
                Mission.img_url,
                Mission.mission_score,
                Mission.is_done
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