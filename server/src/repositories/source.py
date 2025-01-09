from fastapi import HTTPException
from src.models.source import Source
from src.db import SessionLocal
from sqlalchemy import select
from src.schemas.source import ModelSource

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
    def add_source(cls, source: ModelSource) -> Source:
        """
        Добавляет новый источник в базу данных.
        
        :param source: Объект модели источника для добавления.
        :return: Добавленный источник.
        """
        with SessionLocal() as session:
        # Проверяем, существует ли уже источник с таким же URL
            existing_source = session.query(Source).filter(Source.url == source.url).first()
            if existing_source:
                raise HTTPException(status_code=400, detail=f"Source with URL {source.url} already exists.")
        
            data = source.model_dump()
            new_source = Source(**data)

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
            query = select(Source).where(Source.theme == theme)
            returned_source = session.scalar(query)

            if not returned_source:
                raise HTTPException(status_code=404, detail=f"No source found for theme '{theme}'.")
            
            return returned_source.id
        
    @classmethod
    def get_sourse_by_id(cls, id: str) -> Source:
        """
        Получает источник по ID.
        
        :param id: ID источника.
        :return: Источник с указанным ID.
        """
        with SessionLocal() as session:
            query = select(Source).where(Source.id == id)
            returned_source = session.scalar(query)

            if not returned_source:
                raise HTTPException(status_code=404, detail=f"No source found for id '{id}'.")
            
            return returned_source


    @classmethod
    def get_all_sources(cls) -> list[Source]:
        """
        Получает все источники из базы данных.
        
        :return: Список всех источников.
        """
        with SessionLocal() as session:
            query = select(Source)
            result = session.execute(query)

            return result.scalars().all()

    @classmethod
    def update_source(
            cls,
            id: int,
            name: str = None,
            theme: str = None,
            url: str = None
    ) -> Source:
        """
        Обновляет источник по ID.
        
        :param id: ID источника, который нужно обновить.
        :param name: Новое имя источника.
        :param theme: Новая тема источника.
        :param url: Новый URL источника.
        :return: Обновлённый источник.
        """
        with SessionLocal() as session:
            query = select(Source).where(Source.id == id)
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
    def delete_source(cls, id: int) -> Source:
        """
        Удаляет источник по ID.
        
        :param id: ID источника для удаления.
        :return: Удалённый источник.
        """
        with SessionLocal() as session:
            # Проверяем, существует ли источник
            returned_source = session.query(Source).filter(Source.id == id).first()
            if not returned_source:
                raise HTTPException(status_code=404, detail=f"Source with ID {id} not found.")
        
            query = select(Source).where(Source.id == id)
            returned_source = session.scalar(query)

            session.delete(returned_source)

            session.flush()
            session.commit()

            return returned_source
