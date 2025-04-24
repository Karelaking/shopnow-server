from fastapi import APIRouter

userRouter: APIRouter = APIRouter(prefix="/user", tags=["user"])


@userRouter.post("/")
async def createUser():
	...


@userRouter.post("/")
async def loginUser():
	...


@userRouter.post("/")
async def logoutUser():
	...


@userRouter.patch("/")
async def updateUser():
	...


@userRouter.get("/{user_id}")
async def getCurrentUser(user_id: str):
	...


@userRouter.delete("/{user_id")
async def deleteUser(user_id: str):
	...
