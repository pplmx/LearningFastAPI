from fastapi import APIRouter

router = APIRouter()


# add healthz and ready endpoints
@router.get("/healthz")
async def healthz():
    return {"status": "ok"}


@router.get("/ready")
async def ready():
    return {"status": "ok"}
