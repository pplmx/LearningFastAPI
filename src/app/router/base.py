from fastapi import APIRouter

router = APIRouter()


# add livez and ready endpoints
@router.get("/livez")
async def livez():
    return {"status": "ok"}


@router.get("/ready")
async def ready():
    return {"status": "ok"}
