from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/")
async def create_user():
    return "hello"

# @app.post("/")
# async def create_user(
#     body: User,
#     usecase: ICreateUserUsecase = Depends(di_container.resolve(ICreateUserUsecase))
    
# )->Response[UserPublic]:
#     user = await usecase.create_user(body)
#     user_public = UserPublic.from_orm(user)    
#     return Response[UserPublic](data=user_public)



