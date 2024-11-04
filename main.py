from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


# Пример данных для татуировок
tattoos = [
    {"id": 1, "title": "Татуировка дракона", "description": "Реалистичный дракон с японскими мотивами.", "image": "/static/images/dragon_tattoo.jpg"},
    {"id": 2, "title": "Татуировка с цветами", "description": "Цветочный орнамент в черно-белом стиле.", "image": "/static/images/flower_tattoo.jpg"},
    # Добавьте другие татуировки по необходимости
]


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

# @app.get("/portfolio", response_class=HTMLResponse)
# async def portfolio(request: Request):
#     images = ["tattoo1.jpg", "tattoo2.jpg","tattoo3.jpg","tattoo4.jpg","tattoo5.jpg","tattoo6.jpg","tattoo7.jpg","tattoo8.jpg","tattoo9.jpg"]
#     return templates.TemplateResponse("portfolio.html", {"request": request, "images": images})

@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio(request: Request):
    return templates.TemplateResponse("portfolio.html", {"request": request, "tattoos": tattoos})

@app.get("/tattoo/{tattoo_id}", response_class=HTMLResponse)
async def tattoo_detail(request: Request, tattoo_id: int):
    tattoo = next((t for t in tattoos if t["id"] == tattoo_id), None)
    if not tattoo:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("tattoo_detail.html", {"request": request, "tattoo": tattoo})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/booking", response_class=HTMLResponse)
async def booking(request: Request):
    return templates.TemplateResponse("booking.html", {"request": request})

@app.post("/booking", response_class=HTMLResponse)
async def handle_booking(request: Request, name: str = Form(...), email: str = Form(...), message:str = Form(...)):
    print(f"Запись от {name}, email: {email}, сообщение: {message}")
    return RedirectResponse("/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

