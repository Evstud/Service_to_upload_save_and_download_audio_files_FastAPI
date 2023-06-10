import aiohttp
import asyncio
from aiohttp import FormData
import base64


async def send_user_name(user_name):
    url = f'http://127.0.0.1:8001/create_user/'
    headers = {'Content_Type': 'application/json'}
    data = {"user_name": user_name}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=data, headers=headers) as response:
            response_json = await response.json()
            print(response_json)
            return response_json


async def send_audio_file(user_id, user_token, filepath):
    async with aiohttp.ClientSession() as session:
        async with aiohttp.request(
                "POST",
                f'http://127.0.0.1:8001/create_audio/user_id/{user_id}/user_token/{user_token}/',
                data=FormData({'file': open(filepath, 'rb')})) as resp:
            response = await resp.json()
            print(response)
            return response


async def get_mp3(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                resp_json = await resp.json()
                with open(f"new_mp3_files/{resp_json['audio_name']}", 'wb') as f:
                    f.write(base64.b64decode(resp_json['audio_data']))


if __name__ == "__main__":
    # asyncio.run(send_user_name("fourth_user"))
    # asyncio.run(send_audio_file(
    #     url="http://127.0.0.1:8001/create_audio/",
    #     filename='sample-15s2.wav',
    #     filepath='/home/evstud/Different_different/Downloads/sample-15s2.wav',
    #     user_id='4916e250-177f-4dc0-9316-04abcfdb632f',
    #     user_token='3c81ea37-769d-40d6-84be-a624adb051a7'
    # ))
    # asyncio.run(send_audio_file(
    #     filepath="/home/evstud/Different_different/Downloads/sample-15s4.wav",
    #     user_id="4276f65a-511e-4143-a39c-2bfd054fad57",
    #     user_token="a54cbf3e-ddcc-43a9-a30b-68838bd8c4fb"
    # ))
    asyncio.run(get_mp3(
        url="http://127.0.0.1:8001/record?id=c6e458f1-3b37-4ec8-a7a6-05df7b33cc00&user=4276f65a-511e-4143-a39c-2bfd054fad57"
    ))
