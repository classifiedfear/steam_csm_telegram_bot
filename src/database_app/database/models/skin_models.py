from __future__ import annotations

from typing import List

import sqlalchemy
from sqlalchemy import orm

from src.database_app.database.base.declar_base import Base


class WeaponSkinQuality(Base):
    __tablename__ = 'weapon_skin_quality'

    weapon_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.ForeignKey('weapon.id', ondelete='cascade'), primary_key=True, nullable=False
    )
    skin_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.ForeignKey('skin.id', ondelete='cascade'), primary_key=True, nullable=False
    )
    quality_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.ForeignKey('quality.id', ondelete='cascade'), primary_key=True, nullable=False
    )

    weapon: orm.Mapped['Weapon'] = orm.relationship('Weapon', back_populates='w_s_q')
    skin: orm.Mapped['Skin'] = orm.relationship('Skin', back_populates='w_s_q')
    quality: orm.Mapped['Quality'] = orm.relationship('Quality', back_populates='w_s_q')


class Weapon(Base):
    __tablename__ = 'weapon'

    id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer, primary_key=True, nullable=False, unique=True)

    name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String, unique=True, nullable=False)

    w_s_q: orm.Mapped[List['WeaponSkinQuality']] = orm.relationship(
        'WeaponSkinQuality', back_populates='weapon', cascade='all, delete', passive_deletes=True
    )


class Skin(Base):
    __tablename__ = 'skin'

    id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer, primary_key=True, nullable=False, unique=True)

    name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String, nullable=False, unique=True)

    stattrak_existence: orm.Mapped[bool] = orm.mapped_column(sqlalchemy.Boolean, nullable=False)

    w_s_q: orm.Mapped[List['WeaponSkinQuality']] = orm.relationship(
        'WeaponSkinQuality', back_populates='skin', cascade='all, delete', passive_deletes=True
    )


class Quality(Base):
    __tablename__ = 'quality'

    id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer, primary_key=True, nullable=False, unique=True)

    name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String, unique=True, nullable=False)

    w_s_q: orm.Mapped[List['WeaponSkinQuality']] = orm.relationship(
        'WeaponSkinQuality', back_populates='quality', cascade='all, delete', passive_deletes=True
    )

