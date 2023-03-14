#!/usr/bin/env python3
"""Module to define the cardTransaction class"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from datetime import datetime
from models.card import Base


class CardTransaction(Base):
    """Representation of virtual card transaction model class
    """
    __tablename__ = "cardTransactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(Integer, ForeignKey('cards.id'), nullable=False)
    transaction_type = Column(String(10), nullable=False)
    description = Column(String(60), nullable=True)
    currency = Column(String(10), nullable=False)
    amount = Column(String(15), nullable=False)
    datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(10), nullable=False)
