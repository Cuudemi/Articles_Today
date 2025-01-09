from fastapi import FastAPI
import routers as r

app = FastAPI()
app.include_router(r.article_router)
app.include_router(r.source_router)
app.include_router(r.theme_router)

