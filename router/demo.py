from typing import Optional

from fastapi import APIRouter

from model import demo

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, needy: str, q: Optional[str] = None, short: bool = False
):
    """

    :param user_id: Path Parameter
    :param item_id: Path Parameter
    :param needy: required Query Parameter
    :param q: optional Query Parameter
    :param short: optional Query Parameter
    :return:
    """
    item = {"item_id": item_id, "owner_id": user_id, "needy": needy}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@router.get("/models/{model_name}")
async def get_model(model_name: demo.ModelName):
    if model_name == demo.ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
