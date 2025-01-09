from src.repositories.source import SourceRepository
from src.schemas.source import ModelSource, ModelSourceWithID
from fastapi import HTTPException
from tests.unit.fixtures import setup_database
import pytest