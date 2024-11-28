from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from starlette import status

import schemas as schmodel
import models as dbmodel
from db import SessionLocal
from sqlalchemy import select

from Parser.get_articles_by_theme_url import main

class ArticleRepository:

    @classmethod
    def add_today_best_articles(cls, theme: str):
        i = 0
        # получаем нужную ссылку
        id_sourse = SourceRepository.get_id_sourse_by_theme(theme)
        url_sourse = SourceRepository.get_sourse_by_id(id_sourse).url

        articles = main(url_sourse)

        #for article in articles:
        article = articles[0]

        for article in articles:
            new_article = schmodel.ModelArticleWithID(
                id=int(article["id"]),
                name=article["name"],
                id_source=id_sourse,
                content=" ".join(article.get("content", [])),
                url=article["url"],
                theme_name=article["theme"]
            )
            ArticleRepository.add_article(new_article)
            i = i + 1
        return i
            


    @classmethod
    def add_article(cls, article: schmodel.ModelArticle):
        with SessionLocal() as session:
            data = article.model_dump()
            new_article = dbmodel.Article(**data)
            session.add(new_article)
            session.flush()
            session.commit()
            return new_article

    @classmethod
    def get_all_articles(cls):
        with SessionLocal() as session:
            query = select(dbmodel.Article).options(selectinload(dbmodel.Article.source))
            result = session.execute(query)

            return result.scalars().all()

    @classmethod
    def update_article(
            cls,
            id: int,
            name: str = None,
            id_source: int = None,
            content: str = None,
            url: str = None,
            theme: str = None,
    ):
        with SessionLocal() as session:
            query = select(dbmodel.Article).where(dbmodel.Article.id == id)
            returned_article = session.scalar(query)

        if returned_article is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Article not found')

        if name is not None:
            returned_article.name = name
        if id_source is not None:
            returned_article.id_source = id_source
        if content is not None:
            returned_article.content = content
        if url is not None:
            returned_article.url = url
        if theme is not None:
            returned_article.theme = theme

        session.flush()
        session.commit()

        return returned_article

    @classmethod
    def delete_article(cls, id: int):
        with SessionLocal() as session:
            query = select(dbmodel.Article).where(dbmodel.Article.id == id)
            returned_article = session.scalar(query)

            if returned_article is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Article not found')

            session.delete(returned_article)

            session.flush()
            session.commit()

            return returned_article


class ThemeRepository:
    @classmethod
    def add_theme(cls, theme: schmodel.ModelTheme):
        with SessionLocal() as session:
            data = theme.model_dump()
            new_theme = dbmodel.Theme(**data)
            session.add(new_theme)
            session.flush()
            session.commit()
            return new_theme

    @classmethod
    def get_all_themes(cls):
        with SessionLocal() as session:
            query = select(dbmodel.Theme)
            result = session.execute(query)
            return result.scalars().all()

    @classmethod
    def update_theme(cls, name: str, new_name: str):
        with SessionLocal() as session:
            query = select(dbmodel.Theme).where(dbmodel.Theme.name == name)
            returned_theme = session.scalar(query)

            if returned_theme is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Theme not found')

            returned_theme.name = new_name

            session.flush()
            session.commit()

            return returned_theme

    @classmethod
    def delete_theme(cls, name: str):
        with SessionLocal() as session:
            query = select(dbmodel.Theme).where(dbmodel.Theme.name == name)
            returned_theme = session.scalar(query)

            if returned_theme is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Theme not found')

            session.delete(returned_theme)

            session.flush()
            session.commit()

            return returned_theme


class SourceRepository:
    @classmethod
    def get_all_themes(cls):
        sourses = SourceRepository.get_all_themes()
        themes = []
        
        for sourse in sourses:
            theme = sourse.theme
            themes.append(theme)
        return themes

    @classmethod
    def add_source(cls, source: schmodel.ModelSource):
        with SessionLocal() as session:
            data = source.model_dump()
            new_source = dbmodel.Source(**data)

            session.add(new_source)

            session.flush()
            session.commit()

            return new_source
    
    @classmethod
    def get_id_sourse_by_theme(cls, theme: str):
        with SessionLocal() as session:
            query = select(dbmodel.Source).where(dbmodel.Source.theme == theme)
            returned_source = session.scalar(query)

            if returned_source is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Source not found')
            
            return returned_source.id
        
    @classmethod
    def get_sourse_by_id(cls, id: str):
        with SessionLocal() as session:
            query = select(dbmodel.Source).where(dbmodel.Source.id == id)
            returned_source = session.scalar(query)

            if returned_source is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Source not found')
            
            return returned_source


    @classmethod
    def get_all_sources(cls):
        with SessionLocal() as session:
            query = select(dbmodel.Source).options(selectinload(dbmodel.Source.articles))
            result = session.execute(query)

            return result.scalars().all()

    @classmethod
    def update_source(
            cls,
            id: int,
            name: str = None,
            theme: str = None,
            url: str = None
    ):
        with SessionLocal() as session:
            query = select(dbmodel.Source).where(dbmodel.Source.id == id)
            returned_source = session.scalar(query)

            if returned_source is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Source not found')

            if name is not None:
                returned_source.name = name
            if theme is not None:
                returned_source.theme = theme
            if url is not None:
                returned_source.url = url

            session.flush()
            session.commit()

            return returned_source

    @classmethod
    def delete_source(cls, id: int):
        with SessionLocal() as session:
            query = select(dbmodel.Source).where(dbmodel.Source.id == id)
            returned_source = session.scalar(query)

            if returned_source is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Source not found')

            session.delete(returned_source)

            session.flush()
            session.commit()

            return returned_source


