import sqlalchemy as sa

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = '_user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.String, unique=True, nullable=False)
    username = sa.Column(sa.String, unique=True, nullable=False)
    is_superuser = sa.Column(sa.BOOLEAN, default=False)
    password_hash = sa.Column(sa.Text, nullable=False)

    def __repr__(self):
        return self.username


class Task(Base):
    __tablename__ = 'task'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    description = sa.Column(sa.TEXT)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('_user.id'), nullable=False)
    status = sa.Column(
        sa.Enum(
            'new',
            'active',
            'completed',
            name='status_enum'
        ),
        nullable=False,
        default='new',
    )

    def __repr__(self):
        return self.name
