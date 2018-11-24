from src.statistics.db.connector import Connector

from src.statistics.db.table.statmetadata import StatMetaData

conn = Connector().get_connection(login="postgres", password="admin")
engine = Connector().get_engine(login="postgres", password="admin")

# coder_table.create(engine)
# result_table.create(engine)
# case_table.create(engine)

StatMetaData().get_metadata().create_all(engine)
