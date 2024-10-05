from fastapi import APIRouter
from fastapi.responses import Response
from core.tts_processor import process_data

router = APIRouter()


@router.post("/upload")
async def upload(data: dict):
    audio_buffer = await process_data(data)
    return Response(content=audio_buffer.getvalue(), media_type="audio/wav")
