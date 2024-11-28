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

theme_router = APIRouter(
    prefix="/theme",
    tags=["Theme"]
)


@article_router.get("/best")
def add_today_best_article(theme: str):
    count = rep.ArticleRepository.add_today_best_articles(theme)
    return {f"Успешно добавлено {count} новых статей"}

@article_router.post("")
def add_article(article: schmodel.ModelArticle = Depends()):
    new_article = rep.ArticleRepository.add_article(article)
    return {"Added article is: ", new_article}


@article_router.get("")
def get_all_articles():
    return rep.ArticleRepository.get_all_articles()


@article_router.put("")
def update_article(
        id: int,
        name: str = None,
        id_source: int = None,
        content: str = None,
        url: str = None,
        theme: str = None,
):
    updated_article = rep.ArticleRepository.update_article(id, name, id_source, content, url, theme)
    return {"Updated article is: ", updated_article}


@article_router.delete("")
def delete_article(id: int):
    deleted_article = rep.ArticleRepository.delete_article(id)
    return {"Deleted article is: ", deleted_article}


@source_router.post("")
def get_all_available_themes():
    available_themes = rep.SourceRepository.get_all_themes()
    return available_themes

def add_source(source: schmodel.ModelSource = Depends()):
    new_source = rep.SourceRepository.add_source(source)
    return {"Added source is: ", new_source}

@source_router.get("")
def get_all_sources():
    return rep.SourceRepository.get_all_sources()

@source_router.get("/get_id")
def get_id_sourse_by_theme(theme: str):
    return rep.SourceRepository.get_id_sourse_by_theme(theme)

@source_router.get("/get_sourse")
def get_sourse_by_url(id: str):
    return rep.SourceRepository.get_sourse_by_id(id)

@source_router.put("")
def update_source(
        id: int,
        name: str = None,
        theme: str = None,
        url: str = None
):
    updated_source = rep.SourceRepository.update_source(id, name, theme, url)
    return {"Updated source is: ", updated_source}


@source_router.delete("")
def delete_source(id: int):
    deleted_source = rep.SourceRepository.delete_source(id)
    return {"Deleted source is: ", deleted_source}


@theme_router.post("")
def add_theme(theme: schmodel.ModelTheme = Depends()):
    new_theme = rep.ThemeRepository.add_theme(theme)
    return {"Added theme is: ", new_theme}


@theme_router.get("")
def get_all_themes():
    return rep.ThemeRepository.get_all_themes()


@theme_router.put("")
def update_theme(
        name: str,
        new_name: str
):
    updated_theme = rep.ThemeRepository.update_theme(name, new_name)
    return {"Updated theme is: ", updated_theme}


@theme_router.delete("")
def delete_theme(name: str):
    deleted_theme = rep.ThemeRepository.delete_theme(name)
    return {"Deleted theme is: ", deleted_theme}


