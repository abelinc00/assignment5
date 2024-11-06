from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column


class Sandwich(Base):
    __tablename__ = "sandwiches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_name: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(4, 2), nullable=False, server_default="0.0")

    recipes = relationship("Recipe", back_populates="sandwich")
    order_details = relationship("OrderDetail", back_populates="sandwich")


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    item: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, index=True, nullable=False, server_default="0")

    recipes = relationship("Recipe", back_populates="resource")


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id: Mapped[int] = mapped_column(Integer, ForeignKey("sandwiches.id"))
    resource_id: Mapped[int] = mapped_column(Integer, ForeignKey("resources.id"))
    amount: Mapped[int] = mapped_column(Integer, index=True, nullable=False, server_default="0")

    sandwich = relationship("Sandwich", back_populates="recipes")
    resource = relationship("Resource", back_populates="recipes")


class OrderBase(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    total_amount: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    __tablename__ = 'orders_update'

    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'), primary_key=True)
    customer_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    order = relationship("Order", backref="updates")


class Order(OrderBase):
    id: Mapped[int]
    order_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    id = mapped_column(Integer, ForeignKey('orders.id'), primary_key=True, use_existing_column=True)
