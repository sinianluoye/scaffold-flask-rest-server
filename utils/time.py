from datetime import datetime, timezone
from sqlalchemy import TypeDecorator, String

class ISODatetime(TypeDecorator):
    impl = String(40)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.isoformat()

    def process_result_value(self, value, dialect):
        if value is not None:
            return datetime.fromisoformat(value)

def datetime_utcnow():
    return datetime.now(timezone.utc) 

def timestime_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc)