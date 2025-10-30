


from sqlalchemy import  create_engine
class IDEASQLConnection:
    _instance = None
    def __init__(self):
        self.database_url=f'mysql+pymysql://root:sameer12@localhost:3306/skillciti_training'

        self._sql_connection='None'
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    @classmethod
    def get_mysqlconnection(self):
        database_url = f'mysql+pymysql://root:sameer12@localhost:3306/skillciti_training'
        print("hello")
        print(database_url)
        _engine = create_engine(database_url, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=1800)
        return _engine


IDEASQLConnection().get_mysqlconnection()