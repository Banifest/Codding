from src.statistics.db.connector import Connector
from src.statistics.db.table.statmetadata import StatMetaData

engine = Connector().get_engine()

StatMetaData().get_metadata().create_all(engine)
