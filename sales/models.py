from __future__ import annotations

import asyncio
from datetime import date
from decimal import Decimal
from typing import List

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Branch(Base):
    __tablename__ = "branches"

    # Attributes
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Relationships
    sales: Mapped[List[Sale]] = relationship(
        back_populates="branch",
        cascade="all, delete-orphan"
    )


class Sale(Base):
    __tablename__ = "sales"

    # Attributes
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    sale_date: Mapped[date] = mapped_column(
        nullable=False
    )
    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False
    )

    # Relationships
    branch: Mapped[Branch] = relationship(
        back_populates="sales",
        cascade="all, delete-orphan"
    )
    details: Mapped[List[SaleDetail]] = relationship(
        back_populates="sale",
        cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    # Attributes
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    # Relationships
    details: Mapped[List[SaleDetail]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )


class SaleDetail(Base):
    __tablename__ = "sales_details"

    # Attributes
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    sale_id: Mapped[int] = mapped_column(
        ForeignKey("sales.id"),
        nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )
    units: Mapped[float] = mapped_column(
        nullable=False
    )

    # Relationships
    sale: Mapped[Sale] = relationship(
        back_populates="details"
    )
    product: Mapped[Product] = relationship(
        back_populates="details"
    )


if __name__ == "__main__":
    async def main():
        engine = create_async_engine("sqlite+aiosqlite://", echo=True)

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        await engine.dispose()

    asyncio.run(main())
