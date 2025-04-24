from fastapi import APIRouter

productRouter: APIRouter = APIRouter(prefix="products", tags=["products"])


@productRouter.get("/")
async def getAllProducts():
	...


@productRouter.get("/{user_id}")
async def getProductByUser(user_id: str):
	...


@productRouter.get("/{product_id}")
async def getProductById(product_id: str):
	...


@productRouter.post("/")
async def addProduct():
	...


@productRouter.patch("/{product_id}")
async def updateProduct(product_id: str):
	...


@productRouter.delete("/{product_id}")
async def deleteProduct(product_id: str):
	...
