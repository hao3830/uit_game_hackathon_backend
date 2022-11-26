from fastapi import APIRouter, Form

from src.models.mission.mission import Mission
from src.models.user.user import User
from src.models.joiner.joiner import Joiner
from src.rcode import rcode

router = APIRouter()


@router.get('/pending_task')
def get_pending_task_task():
    err, missions = Mission.get_all_pending()

    if err:
        return rcode(err)
    
    return {
        **rcode(1000),
        'missions': missions
    }

@router.get('/completed')
def report_completed(
    user_id: int,
    mission_id: int
):  
    # err, joiner = Joiner.get_all_by_user_id(user_id=user._id)
    
    err, task = Mission.get_all_mission_by_id(mission_id)
    if err:
        return rcode(err)

    err,_ = User.update_score(user_id=user_id,score=task.mission_score)

    if err:
        return rcode(err)

    err,_ = Mission.update_status_mission(status=1,mission_id=mission_id)

    if err:
        return rcode(err)

    return rcode(1000)

@router.get("/user_mission")
def get_mission_by_user_id(
    user_id: int,
):
    err, joiners = Joiner.get_all_by_user_id(user_id=user_id)

    if err:
        return rcode(err)
    
    list_mission = []

    for joiner in joiners:
        err, mission = Mission.get_all_mission_by_id(joiner.mission_id)

        if err:
            return rcode(err)
        
        list_mission.append(mission)

    return {
        **rcode(1000),
        'missions': list_mission
    }


