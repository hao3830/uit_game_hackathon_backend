from fastapi import APIRouter, Form

from src.models.mission.mission import Mission
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
def report_completed():

    return rcode(1000)