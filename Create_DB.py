from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema

def createDatabase(conn_string):
    connectable = create_engine(conn_string)

    with connectable.connect() as connection:
        connection.execute(CreateSchema("clinicproject", if_not_exists=True))
        connection.commit()