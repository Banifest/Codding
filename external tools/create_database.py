from src.config.config_processor import ConfigProcessor
from src.statistics.db.connector import Connector
from src.statistics.db.statmetadata import StatMetaData


def init_db():
    ConfigProcessor().parse_config("""..\\""")
    engine = Connector().get_engine()
    StatMetaData().metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
