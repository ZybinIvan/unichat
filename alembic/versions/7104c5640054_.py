"""empty message

Revision ID: 7104c5640054
Revises: 092490939dd0
Create Date: 2025-05-16 07:41:09.138988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7104c5640054'
down_revision: Union[str, None] = '092490939dd0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# определяем ENUM-тип один раз
role_enum = sa.Enum(
    'USER',
    'STUDENT',
    'TEACHER',
    'UNIVERSITY_ADMIN',
    name='role'
)


def upgrade() -> None:
    """Upgrade schema."""
    # создаём новую таблицу админов
    op.create_table(
        'university_admin',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('university_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['university_id'], ['university.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('university_id')
    )

    # убираем из university поля, которые теперь в UserModel/UniversityAdminModel
    op.drop_constraint('university_email_key', 'university', type_='unique')
    op.drop_column('university', 'first_name')
    op.drop_column('university', 'email')
    op.drop_column('university', 'patronymic')
    op.drop_column('university', 'last_name')
    op.drop_column('university', 'password')

    # создаём ENUM-тип в БД перед тем, как его использовать
    role_enum.create(op.get_bind(), checkfirst=True)

    # меняем тип колонки user.role со строкового на ENUM('USER', 'STUDENT', ...)
    op.alter_column(
        'user', 'role',
        existing_type=sa.VARCHAR(length=50),
        type_=role_enum,
        existing_nullable=False,
        postgresql_using="UPPER(role)::role"
    )


def downgrade() -> None:
    """Downgrade schema."""
    # возвращаем строковый тип для user.role
    op.alter_column(
        'user', 'role',
        existing_type=role_enum,
        type_=sa.VARCHAR(length=50),
        existing_nullable=False,
        postgresql_using="role::text"
    )

    # удаляем ENUM-тип из БД после ALTER
    role_enum.drop(op.get_bind(), checkfirst=True)

    # возвращаем поля university
    op.add_column('university', sa.Column('password', sa.VARCHAR(length=255), nullable=False))
    op.add_column('university', sa.Column('last_name', sa.VARCHAR(length=100), nullable=False))
    op.add_column('university', sa.Column('patronymic', sa.VARCHAR(length=100), nullable=True))
    op.add_column('university', sa.Column('email', sa.VARCHAR(length=255), nullable=False))
    op.add_column('university', sa.Column('first_name', sa.VARCHAR(length=100), nullable=False))
    op.create_unique_constraint('university_email_key', 'university', ['email'])

    # удаляем таблицу админов
    op.drop_table('university_admin')
