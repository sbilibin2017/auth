from fastapi import APIRouter, Depends
from src.auth.interfaces.events.worker import IWorker
from src.auth.events.worker import get_worker
from src.auth.events.agents.user import get_user_topic


router = APIRouter(prefix="/api/v1/users", tags=["users"])



@router.post("/")
async def create_user(
    dto: UserAddDTO,
    usecase: IMessageBroker = Depends(get_create_user_usecase),    
):
    user = await usecase.create_user(dto)
    return user


