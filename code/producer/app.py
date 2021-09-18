from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

messages = ['hola', 'mundo']

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
  return templates.TemplateResponse("producer.html", {"request": request, "messages": messages})

@app.post('/', response_class=HTMLResponse)
def submitMessage(request: Request, message: str=Form(...)):
  return templates.TemplateResponse("producer.html", {"request": request, "messages": messages})



