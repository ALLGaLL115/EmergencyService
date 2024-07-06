from sqlalchemy import Column, ForeignKey, Integer, Table

from database import Base


# listeners_notifications = Table(
#     'listeners_notifications', Base.metadata,
#     Column(Integer, ForeignKey('listeners.id'), primary_key=True),
#     Column(Integer, ForeignKey('notifications.id'), primary_key=True)
# )

class ListenersNotifications(Base):
    __tablename__='listeners_notifications'
    listener_id = Column(Integer, ForeignKey('listeners.id'), primary_key=True),
    notification_id = Column(Integer, ForeignKey('notifications.id'), primary_key=True)
