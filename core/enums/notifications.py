from enum import Enum


class NotificationKindEnum(Enum):
    CLIENT_GREETING = "Client greeting"
    EMPLOYEE_GREETING = "Employee greeting"
    ORDER_COMPLETE = "Order complete"
    RESTORE_PASSWORD = "Restore password"
    NEW_FILM = "New film"
    SESSION_CANCELED = "Session canceled"


class NotificationSendStatus(Enum):
    NOT_SENT = "Not sent"
    FAILED = "Failed"
    SENT = "Sent"
