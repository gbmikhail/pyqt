from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, sessionmaker
import datetime


class ServerStorage:
    class AllUsers:
        id = None
        name = None
        last_login = None

        def __init__(self, username):
            self.name = username
            self.last_login = datetime.datetime.now()

    class ActiveUsers:
        id = None
        user = None
        ip_address = None
        port = None
        login_time = None

        def __init__(self, user_id, ip_address, port, login_time):
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time

    class LoginHistory:
        id = None
        name = None
        date_time = None
        ip = None
        port = None

        def __init__(self, name, date, ip, port):
            self.name = name
            self.date_time = date
            self.ip = ip
            self.port = port

    def __init__(self):
        self.database_engine = create_engine('sqlite:///server_base.db3', echo=False, pool_recycle=7200)

        self.metadata = MetaData()

        users_table = Table(
            'Users', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String, unique=True),
            Column('last_login', DateTime)
        )

        active_users_table = Table(
            'Active_users', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('user', ForeignKey('Users.id'), unique=True),
            Column('ip_address', String),
            Column('port', Integer),
            Column('login_time', DateTime)
        )

        user_login_history = Table(
            'Login_history', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', ForeignKey('Users.id')),
            Column('date_time', DateTime),
            Column('ip', String),
            Column('port', String)
        )

        self.metadata.create_all(self.database_engine)
        mapper(self.AllUsers, users_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.LoginHistory, user_login_history)

        session = sessionmaker(bind=self.database_engine)
        self.session = session()

        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port):
        rez = self.session.query(self.AllUsers).filter_by(name=username)
        if rez.count():
            user = rez.first()
            user.last_login = datetime.datetime.now()
        else:
            user = self.AllUsers(username)
            self.session.add(user)
            self.session.commit()

        new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.datetime.now())
        self.session.add(new_active_user)

        history = self.LoginHistory(user.id, datetime.datetime.now(), ip_address, port)
        self.session.add(history)

        self.session.commit()

    def user_logout(self, username):
        user = self.session.query(self.AllUsers).filter_by(name=username).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.commit()

    def users_list(self):
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login,
        )
        return query.all()

    def active_users_list(self):
        query = self.session.query(
            self.AllUsers.name,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
            ).join(self.AllUsers)
        return query.all()

    def login_history(self, username=None):
        query = self.session.query(
            self.AllUsers.name,
            self.LoginHistory.date_time,
            self.LoginHistory.ip,
            self.LoginHistory.port
        ).join(self.AllUsers)
        if username:
            query = query.filter(self.AllUsers.name == username)
        return query.all()


if __name__ == '__main__':
    test_db = ServerStorage()
    test_db.user_login('client_1', '192.168.1.4', 8888)
    test_db.user_login('client_2', '192.168.1.5', 7777)
    print(test_db.active_users_list())
    test_db.user_logout('client_1')
    print(test_db.active_users_list())
    test_db.login_history('client_1')
    print(test_db.users_list())
