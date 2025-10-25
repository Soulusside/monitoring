from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

data = {"temperature": None, "co": None}

class SensorData(BaseModel):
    temperature: float
    co: float

@app.post("/api/data")
def receive_data(d: SensorData):
    global data
    data = d.dict()
    print(data)
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def show_page():
    return f"""
    <html>
    <head><meta charset="utf-8"><title>Мониторинг воздуха</title></head>
    <body style="font-family:sans-serif;text-align:center;">
      <h2>Данные с датчиков</h2>
      <p>Температура: {data['temperature'] or '--'} °C</p>
      <p>CO: {data['co'] or '--'} ppm</p>
      <meta http-equiv="refresh" content="5">
    </body>
    </html>
    """
