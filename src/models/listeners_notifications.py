from sqlalchemy import Column, ForeignKey, Integer, Table

from database import Base



class ListenersNotifications(Base):
    __tablename__='listeners_notifications'
    listener_id = Column(Integer, ForeignKey('listeners.id', ondelete="CASCADE"), primary_key=True)
    notification_id = Column(Integer, ForeignKey('notifications.id', ondelete="CASCADE"), primary_key=True)

    def convert_to_model(self):
        return ListenersNotifications(
            listener_id = self.listener_id,
            notification_id = self.notification_id,
        )
