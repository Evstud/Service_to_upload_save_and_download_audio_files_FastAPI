# import aiohttp

from db import SessionLocal
from models import UserTable, Audio
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException
from pydub import AudioSegment
from decouple import config
from sqlalchemy import LargeBinary
import base64


# Create a session to access the db
def get_db():
    """This function creates a session to access the db."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create_request
async def db_create_user(
        user_name: str,
        db: Session):
    """This function creates an instance in User table. Arguments: user_name (str), db (Session).
    Function returns a dict with user_id, user_token and user_name.
    """
    try:
        db_user = UserTable(
            user_name=user_name
        )
        db.add(db_user)
        db.commit()
    except Exception as ex:
        return ex

    return {
        "user_id": db_user.user_id,
        "user_token": db_user.user_token,
        "user_name": db_user.user_name}


async def db_verify_user(
        user_id: UUID,
        user_token: UUID,
        db: Session):
    """This function verifies if user instance exists. Arguments: user_id (UUID), user_token (UUID), db (Session).
    Function returns 'True' if user with this user_id and user_token exists, and 'False' if not.
    """
    try:
        result = db.query(UserTable).filter(UserTable.user_id == user_id, UserTable.user_token == user_token).first()
    except Exception as ex:
        return HTTPException(status_code=500,
                             detail=f"Exception while verifying user in db: {ex}.")
    else:
        if result is not None:
            return True
        else:
            return False


async def db_save_audio(
        audio_name: str,
        audio_data: bytes,
        user_id: UUID,
        db: Session):
    """Function to save mp3 file in db. Arguments: audio_name (str), audio_data (bytes), user_id (UUID), db (Session).
    Function returns a link with parameters to download mp3 file.
    """
    db_audio = Audio(
        audio_name=audio_name,
        audio_data=audio_data,
        user_id=user_id
    )
    try:
        db.add(db_audio)
        db.commit()
        db.refresh(db_audio)
        link_to_return = f'''http://{config("SOCKET_FOR_LINK")}/record?id={db_audio.audio_id}&user={user_id}'''
        return link_to_return
    except Exception as ex:
        return ex


async def db_get_all_audio(
        db: Session):
    """Function to get audio_id, audio_name and user_id of all instances of Audio table. No arguments.
    Function returns a list of instances of Audio table.
    """
    audios = db.query(Audio).all()
    list_to_return = [[i.audio_name, i.user_id, i.audio_id] for i in audios]
    return list_to_return


async def db_get_audio(
        audio_id: UUID,
        user_id: UUID,
        db: Session):
    """Function to get mp3 file from db. Arguments: audio_id (UUID), user_id (UUID), db (Session).
    Function returns a dict with audio_name (str) and audio_data (a b64encode.decode('utf-8') string).
    """
    audio_instance = db.query(Audio).filter(Audio.audio_id == audio_id, Audio.user_id == user_id).first()
    aud_data = base64.b64encode(audio_instance.audio_data).decode('utf-8')
    aud_name = audio_instance.audio_name
    return {'audio_name': aud_name, 'audio_data': str(aud_data)}
