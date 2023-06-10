import aiohttp
import asyncio
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
                data=aiohttp.FormData({'file': open(filepath, 'rb')})) as resp:
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
    # asyncio.run(send_user_name("first_user"))
    #
    # asyncio.run(send_audio_file(
    #     filepath="/home/evstud/Different_different/Downloads/sample-15s4.wav",
    #     user_id="6e3bd2c9-ed1a-42df-9d4a-826a443f6bfd",
    #     user_token="8eb120ff-d859-402c-b9e8-97f84b3406d7"
    # ))
    #
    asyncio.run(get_mp3(
        url="http://127.0.0.1:8001/record?id=bc5a8361-55d7-4886-a21a-f010bd8691c3&user=69f853d1-b5e9-401c-8cb1-8936d8d08c02"
    ))
