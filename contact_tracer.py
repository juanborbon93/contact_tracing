from fastapi import FastAPI,Form,Response
from modules import reply_to_text,register_organizer,handle_message

app = FastAPI()

@app.post("/hook")
async def chat(From:str=Form(...),Body:str=Form(...)):
    print(From)
    msg = handle_message(Body,From)
    return Response(content=str(msg),media_type="application/xml")
app.post("/new_organizer")(register_organizer)
