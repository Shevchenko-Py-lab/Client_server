from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime


class ServerDatabase:
    server_db = declarative_base()
    # a) все пользователи:
    # *логин;
    # *информация(время последнего входа).

    class AllUsers(server_db):
        __tablename__ = 'all_users'
        id = Column(Integer, primary_key=True)
        login = Column(String, unique=True)
        last_online = Column(DateTime)

        def __init__(self, login):
            self.login = login
            self.last_online = datetime.datetime.now()

    # b) активные пользователи:
    # *id_клиента;
    # * время входа;
    # *ip - адрес;
    # *port.
    class ActiveUsers(server_db):
        __tablename__ = 'active_users'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.id'), unique=True)
        ip = Column(String)
        port = Column(Integer)
        login_time = Column(DateTime)

        def __init__(self, user, ip, port, login_time):
            self.user = user
            self.ip = ip
            self.port = port
            self.login_time = login_time

    # с) история клиента:
    # *id_клиента;
    #  * время входа;
    # *ip - адрес;
    # *port.
    class LoginHistory(server_db):
        __tablename__ = 'login_history'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.id'))
        ip = Column(String)
        port = Column(Integer)
        last_online = Column(DateTime)

        def __init__(self, user, ip, port, last_online):
            self.user = user
            self.ip = ip
            self.port = port
            self.last_online = last_online

    def __init__(self):
        self.engine = create_engine('sqlite:///server_base.db3', echo=True, pool_recycle=7200)

        self.server_db.metadata.create_all(self.engine)
        session_maker = sessionmaker(bind=self.engine)
        self.session = session_maker()

        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port):
        unique_login_check = self.session.query(self.AllUsers).filter_by(login=username)
        if unique_login_check.count():
            user = unique_login_check.first()
            user.last_online = datetime.datetime.now()
        else:
            user = self.AllUsers(username)
            self.session.add(user)
            self.session.commit()

        new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.datetime.now())
        self.session.add(new_active_user)

        history = self.LoginHistory(user.id, ip_address, port, datetime.datetime.now())
        self.session.add(history)

        self.session.commit()

    def user_logout(self, username):
        user = self.session.query(self.AllUsers).filter_by(login=username).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.commit()

    def users_list(self):
        query = self.session.query(
            self.AllUsers.login,
            self.AllUsers.last_online,
        )
        return query.all()

    def active_users_list(self):
        query = self.session.query(
            self.AllUsers.login,
            self.ActiveUsers.ip,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
            ).join(self.AllUsers)
        return query.all()

    def login_history(self, username=None):
        query = self.session.query(self.AllUsers.login,
                                   self.LoginHistory.last_online,
                                   self.LoginHistory.ip,
                                   self.LoginHistory.port
                                   ).join(self.AllUsers)
        if username:
            query = query.filter(self.AllUsers.login == username)
        return query.all()


if __name__ == '__main__':
    db = ServerDatabase()
    db.user_login('client_1', '192.168.1.4', 8888)
    db.user_login('client_2', '192.168.1.5', 7777)
    print(db.active_users_list())
    db.user_logout('client_1')
    print(db.users_list())
    print(db.active_users_list())
    db.user_logout('client_2')
    print(db.users_list())
    print(db.active_users_list())
