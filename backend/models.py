from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime, timezone

from database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)

    user_input = Column(Text, nullable=False)

    pratijna = Column(Text, nullable=False)
    hetu = Column(Text, nullable=False)
    udaharana = Column(Text, nullable=False)
    upanaya = Column(Text, nullable=False)
    nigamana = Column(Text, nullable=False)

    explanation = Column(Text, nullable=False)

    validity = Column(Text, nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )