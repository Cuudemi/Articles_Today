from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from starlette import status

import schemas as schmodel
import models as dbmodel
from db import SessionLocal
from sqlalchemy import select

from Parser import get_articles_by_theme_url

class ArticleRepository:

    @classmethod
    def add_today_best_articles(cls, theme: str) -> int:
        """
        Добавляет лучшие статьи на сегодня для указанной темы. Парсит статьи с помощью функции
        `get_articles_by_theme_url`, затем сохраняет их в базу данных.
        
        :param theme: Тема, для которой нужно получить статьи.
        :return: Количество добавленных статей.
        """
        i = 0
        # получаем нужную ссылку
        id_sourse = SourceRepository.get_id_sourse_by_theme(theme)
        url_sourse = SourceRepository.get_sourse_by_id(id_sourse).url

        articles = get_articles_by_theme_url.main(url_sourse)

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
    def add_article(cls, article: schmodel.ModelArticle) -> dbmodel.Article:
        """
        Добавляет новую статью в базу данных.
        
        :param article: Объект модели статьи для добавления в БД.
        :return: Добавленная статья.
        """
        with SessionLocal() as session:
            data = article.model_dump()
            new_article = dbmodel.Article(**data)
            session.add(new_article)

            session.flush()
            session.commit()

            return new_article

    @classmethod
    def get_all_articles(cls) -> list[dbmodel.Article]:
        """
        Получает все статьи из базы данных.
        
        :return: Список всех статей в базе данных.
        """ 
        with SessionLocal() as session:
            query = select(dbmodel.Article)
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
    ) -> dbmodel.Article:
        """
        Обновляет существующую статью по её ID.
        
        :param id: ID статьи, которую нужно обновить.
        :param name: Новое имя статьи.
        :param id_source: Новый ID источника.
        :param content: Новый контент статьи.
        :param url: Новый URL статьи.
        :param theme: Новая тема статьи.
        :return: Обновленная статья.
        """
        with SessionLocal() as session:
            query = select(dbmodel.Article).where(dbmodel.Article.id == id)
            returned_article = session.scalar(query)

            # Если статья не найдена
            if not returned_article:
                raise HTTPException(status_code=404, detail=f"Article with ID {id} not found.")

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
    def delete_article(cls, id: int) -> dbmodel.Article:
        """
        Удаляет статью по её ID.
        
        :param id: ID статьи для удаления.
        :return: Удалённая статья.
        """
        with SessionLocal() as session:
            # Проверяем, существует ли статья
            returned_article = session.query(dbmodel.Article).filter(dbmodel.Article.id == id).first()
            if not returned_article:
                raise HTTPException(status_code=404, detail=f"Article with ID {id} not found.")
            
            query = select(dbmodel.Article).where(dbmodel.Article.id == id)
            returned_article = session.scalar(query)

            session.delete(returned_article)

            session.flush()
            session.commit()

            return returned_article

class SourceRepository:
    @classmethod
    def get_all_themes(cls) -> list[str]:
        """
        Получает все уникальные темы источников.
        
        :return: Список всех тем.
        """
        sourses = SourceRepository.get_all_themes()
        themes = []
        
        for sourse in sourses:
            theme = sourse.theme
            themes.append(theme)
        return themes

    @classmethod
    def add_source(cls, source: schmodel.ModelSource) -> dbmodel.Source:
        """
        Добавляет новый источник в базу данных.
        
        :param source: Объект модели источника для добавления.
        :return: Добавленный источник.
        """
        # Проверяем, существует ли уже источник с таким же URL
        existing_source = session.query(dbmodel.Source).filter(dbmodel.Source.url == source.url).first()
        if existing_source:
            raise HTTPException(status_code=400, detail=f"Source with URL {source.url} already exists.")
        
        with SessionLocal() as session:
            data = source.model_dump()
            new_source = dbmodel.Source(**data)

            session.add(new_source)

            session.flush()
            session.commit()

            return new_source
    
    @classmethod
    def get_id_sourse_by_theme(cls, theme: str) -> int:
        """
        Получает ID источника по теме.
        
        :param theme: Тема, для которой нужно получить источник.
        :return: ID источника.
        """
        with SessionLocal() as session:
            query = select(dbmodel.Source).where(dbmodel.Source.theme == theme)
            returned_source = session.scalar(query)

            if not returned_source:
                raise HTTPException(status_code=404, detail=f"No source found for theme '{theme}'.")
            
            return returned_source.id
        
    @classmethod
    def get_sourse_by_id(cls, id: str) -> dbmodel.Source:
        """
        Получает источник по ID.
        
        :param id: ID источника.
        :return: Источник с указанным ID.
        """
        with SessionLocal() as session:
            query = select(dbmodel.Source).where(dbmodel.Source.id == id)
            returned_source = session.scalar(query)

            if not returned_source:
                raise HTTPException(status_code=404, detail=f"No source found for id '{id}'.")
            
            return returned_source


    @classmethod
    def get_all_sources(cls) -> list[dbmodel.Source]:
        """
        Получает все источники из базы данных.
        
        :return: Список всех источников.
        """
        with SessionLocal() as session:
            query = select(dbmodel.Source)
            result = session.execute(query)

            return result.scalars().all()

    @classmethod
    def update_source(
            cls,
            id: int,
            name: str = None,
            theme: str = None,
            url: str = None
    ) -> dbmodel.Source:
        """
        Обновляет источник по ID.
        
        :param id: ID источника, который нужно обновить.
        :param name: Новое имя источника.
        :param theme: Новая тема источника.
        :param url: Новый URL источника.
        :return: Обновлённый источник.
        """
        with SessionLocal() as session:
            query = select(dbmodel.Source).where(dbmodel.Source.id == id)
            returned_source = session.scalar(query)

            # Если статья не найдена
            if not returned_source:
                raise HTTPException(status_code=404, detail=f"Source with ID {id} not found.")

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
    def delete_source(cls, id: int) -> dbmodel.Source:
        """
        Удаляет источник по ID.
        
        :param id: ID источника для удаления.
        :return: Удалённый источник.
        """
        with SessionLocal() as session:
            # Проверяем, существует ли источник
            returned_source = session.query(dbmodel.Source).filter(dbmodel.Source.id == id).first()
            if not returned_source:
                raise HTTPException(status_code=404, detail=f"Source with ID {id} not found.")
        
            query = select(dbmodel.Source).where(dbmodel.Source.id == id)
            returned_source = session.scalar(query)

            session.delete(returned_source)

            session.flush()
            session.commit()

            return returned_source


