from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import signpdf, verifypdf

app = FastAPI(version="0.1.0")


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    signpdf.router,
    prefix="/pdf"
)

app.include_router(
    verifypdf.router,
    prefix="/pdf"
)

@app.get("/")
async def root():
    return {"Greetings": "Hey! Thank you for using this service. If you don't know how to use it, check out readme on "
                         "Github.",
            "Repository": "https://github.com/Adrixop95/Barcode-Service/",
            "MOTD": "Have a nice day : D"
            }
