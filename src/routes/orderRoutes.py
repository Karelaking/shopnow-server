from fastapi import APIRouter

orderRouter: APIRouter = APIRouter(prefix="orders", tags=["orders"])


@orderRouter.get("/{user_id}")
async def getAllOrders(user_id: str):
	...


@orderRouter.get("/{order_id}")
async def getOrder(order_id: str):
	...


@orderRouter.patch("/{order_id}")
async def updateOrder(order_id: str):
	...


@orderRouter.delete("/{order_id}")
async def deleteOrder(order_id: str):
	...
