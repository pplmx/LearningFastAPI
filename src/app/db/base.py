from model.user import User
from sqlmodel import Session, SQLModel, create_engine, select

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db():
    create_db_and_tables()
    create_users()


def recreate_db():
    drop_all()
    create_db()


def drop_all():
    SQLModel.metadata.drop_all(engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# pre-populate the database with some users
def create_users():
    with Session(engine) as session:
        # if the database is empty, create some users
        if session.exec(select(User)).first() is not None:
            return
        user_0 = User(name="Administrator", email="admin@x.io", password="secret")
        user_1 = User(name="John", email="John@x.io", password="secret")
        user_2 = User(name="Susan", email="Susan@x.io", password="secret")
        user_3 = User(name="Mary", email="Mary@x.io", password="secret")

        session.add_all([user_0, user_1, user_2, user_3])
        session.commit()


def get_user_by_email(email: str):
    with Session(engine) as session:
        user = session.query(User).filter(User.email == email).first()
        return user
