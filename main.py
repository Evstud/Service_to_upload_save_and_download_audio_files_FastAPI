import logging
import magic
import os

from uuid import UUID
from schemas import BaseUser
from db_funcs import get_db, db_create_user, db_save_audio, db_verify_user, db_get_audio, db_get_all_audio
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from pydub import AudioSegment

app = FastAPI(title='Questions_handler')

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=u'[%(asctime)s] - %(message)s')
logger.info("Start service")


@app.post("/create_user/", tags=['User'], description='Endpoint to create user')
async def create_user(message: BaseUser, db: Session = Depends(get_db)):
    """Function to create user. It handles an incoming message with 'username', call db function to create a new user
    and returns it.
    """
    user_name = message.user_name
    result = await db_create_user(user_name=user_name, db=db)
    if not isinstance(result, dict):
        raise HTTPException(status_code=500,
                            detail=f"Exception is: {result}.")
    else:
        return result


@app.post(
    "/create_audio/user_id/{user_id}/user_token/{user_token}/",
    tags=['Audio'],
    description='Endpoint to create audio.')
async def save_audio(user_id: UUID, user_token: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Function to convert wav file to mp3 file and to save it in db. It receives user_id, user_token and 'wav'
    file with file_name, converts it into 'mp3' format and calls a db function to saves it in db and get a link
    to download this instance from db. Preliminary this function calls another function to verify if user is in db.
    """
    if file.content_type not in ['audio/x-wav', 'audio/wav']:
        return {"error": "Unsupported file format."}

    if await db_verify_user(
            user_id=user_id,
            user_token=user_token,
            db=db):
        mp3_name = file.filename.split('.')[0] + '.mp3'
        AudioSegment.from_wav(file.file).export(f"temp/{mp3_name}", format="mp3")
        with open(f'temp/{mp3_name}', mode="rb") as file:
            binary_content = file.read()
        try:
            result = await db_save_audio(
                audio_name=mp3_name,
                audio_data=binary_content,
                user_id=user_id,
                db=db)
            file_path = f'temp/{mp3_name}'
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"Error: {e.filename}-{e.strerror}.")
            else:
                print(f"The file {file_path} does not exist.")
            if result:
                return result
            else:
                raise HTTPException(status_code=500,
                                    detail=f"Exception while saving mp3 file: {result}.")
        except Exception as ex:
            raise HTTPException(status_code=500,
                                detail=f"Exception while saving mp3 file: {ex}.")
    else:
        raise HTTPException(status_code=404,
                            detail=f"User {user_id} is not registered.")


@app.get("/audios/", tags=['Audio'], description='Endpoint to get all instances of Audio table')
async def get_all_audios(db: Session = Depends(get_db)):
    """This function calls a db function to get audio_id, audio_name and user_id of all instances of Audio table."""
    result = await db_get_all_audio(db=db)
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail=f"Instances of Audio table are not found.")


@app.get("/record", tags=['Audio'], description='Endpoint to get an instance of Audio table from db.')
async def get_audio(
        id: UUID,
        user: UUID,
        db: Session = Depends(get_db)):
    """This function calls a db function to get an instance of Audio table by audio_id and user_id.
    Arguments: id (UUID, audio_id), user (UUID, user_id), db (Session)."""
    result = await db_get_audio(
        audio_id=id,
        user_id=user,
        db=db
    )
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail=f"No instances by id: {id} and user: {user} found.")
