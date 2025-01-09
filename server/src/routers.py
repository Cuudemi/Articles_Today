"""
роутеры FastAPI для сущностей API
"""

import repositories as rep
import schemas as schmodel
from fastapi import APIRouter, Depends

article_router = APIRouter(
    prefix="/article",
    tags=["Article"]
)

source_router = APIRouter(
    prefix="/source",
    tags=["Source"]
)

@article_router.post("/article/add_today_best_article/")
def add_today_best_article(theme: str):
    count = rep.ArticleRepository.add_today_best_articles(theme)
    return {count}

@article_router.post("/article/add_article/")
def add_article(article: schmodel.ModelArticle = Depends()):
    new_article = rep.ArticleRepository.add_article(article)
    return new_article

@article_router.get("/article/get_all_articles/")
def get_all_articles():
    return rep.ArticleRepository.get_all_articles()

@article_router.put("/article/update_article/")
def update_article(
        id: int,
        name: str = None,
        id_source: int = None,
        content: str = None,
        url: str = None,
        theme: str = None,
):
    updated_article = rep.ArticleRepository.update_article(id, name, id_source, content, url, theme)
    return updated_article

@article_router.delete("/article/delete_article/")
def delete_article(id: int):
    deleted_article = rep.ArticleRepository.delete_article(id)
    return deleted_article

@source_router.get("/source/get_all_available_themes/")
def get_all_available_themes():
    available_themes = rep.SourceRepository.get_all_themes()
    return available_themes

@source_router.get("/source/get_id_sourse_by_theme/")
def get_id_sourse_by_theme(theme: str):
    return rep.SourceRepository.get_id_sourse_by_theme(theme)

@source_router.get("source/get_sourse_by_url")
def get_sourse_by_url(id: str):
    return rep.SourceRepository.get_sourse_by_id(id)

@source_router.post("/source/get_all_available_themes/")
def add_source(source: schmodel.ModelSource = Depends()):
    new_source = rep.SourceRepository.add_source(source)
    return new_source

@source_router.get("/source/get_all_sources/")
def get_all_sources():
    return rep.SourceRepository.get_all_sources()

@source_router.put("/source/update_source/")
def update_source(
        id: int,
        name: str = None,
        theme: str = None,
        url: str = None
):
    updated_source = rep.SourceRepository.update_source(id, name, theme, url)
    return updated_source

@source_router.delete("/source/delete_source/")
def delete_source(id: int):
    deleted_source = rep.SourceRepository.delete_source(id)
    return deleted_source