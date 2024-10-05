from fastapi import APIRouter
from core.tts_processor import process_data

router = APIRouter()

@router.post("/upload")
async def upload(data: dict):
    return await process_data(data)