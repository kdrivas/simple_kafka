from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.get('/')
def index(response_class=HTMLResponse):
  return templates.TemplateResponse("producer.html")

