#!/usr/bin/env python3
"""The Database module"""
from os import getenv
import random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from flask import Flask
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from typing import List
from models.cardTransaction import CardTransaction
from models.card import Base, Card

class DB:
    """Database Connector class"""
    def __init__(self) -> None:
        """Initialises a new DB instance"""
        DB_USER = getenv("DB_USER")
        DB_PWD = getenv("DB_PWD")
        DB_NAME = getenv("DB_NAME")
        ENV = getenv("ENV")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}"
                                      .format(DB_USER, DB_PWD, DB_NAME))

        if "ENV" == "test":
            Base.metadata.drop_all(self.__engine)

        Base.metadata.create_all(self.__engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self.__engine)
            self.__session = DBSession()
        return self.__session

    def create_card(self, acct_id: int, brand: str, currency: str, name: str, pin: int) -> Card:
        """Add a new card to the database"""
        card_number = str(random.randint(1, 100000000000000000))#Build a better generator later
        date_created = datetime.utcnow()
        date_updated = date_created
        status = "inactive" #default value
        balance = "30000.00" #subject to change
        cvv = random.randint(0, 3) #Build a better generator later
        expiry_date = datetime.utcnow() #Build a function to set expiry date based on date_created
        card = Card(account_id=acct_id, card_brand=brand, card_currency=currency,
                    name_on_card=name, pin=pin,
                    date_created=date_created, date_updated=date_updated,
                    status=status, cvv=cvv, card_number=card_number, expiry_date=expiry_date,
                    balance=balance)
        self._session.add(card)
        self._session.commit()
        return card

    def fund_card(self, card_id: int, amount: str, transaction_type: str, narration: str, currency: str, status: str) -> CardTransaction:
        """Attempts to fund a card from a wallet"""
        datetime_created = datetime.utcnow()
        datetime_updated = datetime.utcnow()
        cardTransaction = CardTransaction(card_id=card_id, transaction_type=transaction_type,
                                          amount=amount, currency=currency, status=status,
                                          description=narration, 
                                          datetime_created=datetime_created, 
                                          datetime_updated=datetime_updated)
        self._session.add(cardTransaction)
        self._session.commit()
        return cardTransaction

    def find_card_by(self, **kwargs) -> Card:
        """Find card from DB by key-value pairs argument"""
        if not kwargs or not self.valid_query_args(**kwargs):
            raise InvalidRequestError

        card = self._session.query(Card).filter_by(**kwargs)

        if not card:
            raise NoResultFound
        return card

    def update_card(self, card_id: int, **kwargs) -> None:
        """Update card details based on card ID"""
        if not self.valid_query_args(**kwargs):
            raise ValueError

        card = self.find_card_by(id=card_id)

        for key, value in kwargs.items():
            setattr(card, key, value)

        self._session.commit()


    def all_cards(self) -> List[Card]:
        """Returns all cards"""
        objs = []
        cards = self._session.query(Card).all()
        for card in cards:
            obj = card.__dict__.copy()
            if obj['_sa_instance_state']:
                del obj['_sa_instance_state']
            objs.append(obj)
        return objs

    def all_cardTransactions(self) -> List[CardTransaction]:
        """Returns all cards"""
        objs = []
        cards = self._session.query(CardTransaction).all()
        for card in cards:
            obj = card.__dict__.copy()
            if obj['_sa_instance_state']:
                del obj['_sa_instance_state']
            objs.append(obj)
        return objs


    def valid_query_args(self, **kwargs):
        """Get table columns or keys"""
        columns = Card.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in columns:
                return False
        return True
