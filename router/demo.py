from typing import Optional

from fastapi import APIRouter, Query, status

from model.demo import Item, ModelName

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/items/")
async def read_items(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@router.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, needy: str, q: Optional[str] = None, short: bool = False
):
    """
        read users items
    :param user_id: Path Parameter user_id
    :param item_id: Path Parameter item_id
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
async def get_model(model_name: ModelName):
    if model_name == ModelName.AlexNet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "LeNet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@router.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags")
async def create_item1(item: Item):
    """
        only Request body
    :param item:
    :return:
    """
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@router.put("/items/{item_id}")
async def create_item2(item_id: int, item: Item, q: Optional[str] = None):
    """
        Request body + path + query parameters
    :param item_id:
    :param item:
    :param q:
    :return:
    """
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
