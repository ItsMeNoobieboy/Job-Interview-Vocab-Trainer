import asyncio
import json
from Translator import Translator
from websockets.exceptions import ConnectionClosed
from websockets.server import serve
from ChatGPTResponse import GPT

gpts = dict()

OP_CODE = {
    "DESTROY": 0,
    "CREATE": 1,
    "SEND": 2,
    "NEW_RESPONSE": 3,
    "ADD_RESPONSE": 4,
    "FINISH_RESPONSE": 5,
    "TRANSLATE": 6
}

async def handler(websocket):
    try:
        async for request in websocket:
            request, message = json.loads(request)
            translator = True
            
            client_id = websocket.id

            if request == OP_CODE["DESTROY"]:
                if client_id in gpts:
                    del gpts[client_id]
            elif request == OP_CODE["CREATE"]:
                if client_id not in gpts:
                    gpts[client_id] = {"gpt": GPT(), "count": 0, "translator": None}
                await websocket.send(json.dumps([OP_CODE["NEW_RESPONSE"], ""]))
                await websocket.send(json.dumps([OP_CODE["ADD_RESPONSE"], "Thank you for coming in today. I understand that you're interested in working at our company. Can you please start by telling me which position you are applying for?"]))
                await websocket.send(json.dumps([OP_CODE["FINISH_RESPONSE"], str(gpts[client_id]["count"])]))
            elif request == OP_CODE["SEND"]:
                if client_id not in gpts:
                    gpts[client_id] = {"gpt": GPT(), "count": 0, "translator": None}
                
                gpts[client_id]["count"] += 1
                await websocket.send(json.dumps([OP_CODE["NEW_RESPONSE"], ""]))
                for chunk in gpts[client_id]["gpt"].get_completion(message):
                    await websocket.send(json.dumps([OP_CODE["ADD_RESPONSE"], chunk]))
                await websocket.send(json.dumps([OP_CODE["FINISH_RESPONSE"], str(gpts[client_id]["count"])]))
                
            elif request == OP_CODE["TRANSLATE"]:
                print(message)
                if Translator is not None:
                    translator = Translator(message["lang"])
                res = []
                for word in message["words"]:
                    res.append(translator.translate_to_native(word))
                print(res)
                await websocket.send(json.dumps([OP_CODE["TRANSLATE"], res]))

    except ConnectionClosed:
        print("Client disconnected. Do cleanup")
        if websocket.id in gpts:
            del gpts[websocket.id]     

async def main():
    async with serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
    print("Server started!")
