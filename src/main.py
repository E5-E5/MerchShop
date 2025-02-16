from fastapi import FastAPI, Depends
from .controller import buy_item, auth, send_coins, info  # Импортируйте ваш API роутер


app = FastAPI()

app.include_router(buy_item.router)
app.include_router(auth.router)
app.include_router(info.router)
app.include_router(send_coins.router)


@app.get("/")
def read_root():
    return {"message": "MerchShop"}
