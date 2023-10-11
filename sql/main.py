from sqlalchemy import create_engine
from sklearn.datasets import fetch_openml

def main():
    engine = create_engine("sqlite:///sqlite.db", echo=True)
    connection = engine.connect()

    X1,y = fetch_openml(data_id=43592,return_X_y=True,as_frame=True,
                    parser='auto')

    sqlite_table = "fake_news"
    X1.to_sql(sqlite_table, connection, if_exists='replace')

    connection.close()
    return

if __name__=='__main__':
    main()