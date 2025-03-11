from collections import defaultdict
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import aiosmtplib
from jinja2 import Environment, FileSystemLoader

from apps.notifications.models.notification import Notification
from core.config import config
from core.enums.notifications import NotificationSendStatus
from core.loggers.base import BaseLogger


@dataclass
class BaseMailClient:
    async def notify(
        self, notification: Notification, template: str, kwargs: dict = None
    ) -> None:
        """Переопределить в дочерних классах"""

    async def _validate(self, errors: dict[list]) -> None:
        """Переопределить в дочерних классах"""

    async def _notify(self) -> None:
        """Переопределить в дочерних классах"""


@dataclass
class MailClient(BaseMailClient):
    logger: BaseLogger

    smtp_server = config.SMTP_SERVER
    smtp_port = config.SMTP_PORT
    smtp_username = config.SMTP_USERNAME
    smtp_password = config.SMTP_PASSWORD
    template_folder = Path(__file__).resolve().parents[2] / "templates"

    async def notify(
        self, notification: Notification, template: str, kwargs: dict = None
    ):
        self.notification = notification
        self.kwargs = kwargs
        self.template = template

        errors = defaultdict(list)
        await self._validate(errors)
        if errors:
            self.logger.error(
                f"Произошла ошибка при отправке уведомления. Ошибка - {errors}"
            )
        else:
            await self._notify()

    async def _validate(self, errors: dict[list]):
        if self.notification.send_status == NotificationSendStatus.SENT:
            errors["notification_already_sent"] = (
                "Уведомление уже было отправлено"
            )

    async def _notify(self) -> None:
        env = Environment(loader=FileSystemLoader(self.template_folder))
        template = env.get_template(self.template)
        body = template.render(**self.kwargs)

        msg = MIMEMultipart()
        msg["From"] = self.smtp_username
        msg["To"] = self.notification.email
        msg["Subject"] = self.notification.title

        msg.attach(MIMEText(body, "html"))

        try:
            await aiosmtplib.send(
                msg,
                hostname=self.smtp_server,
                port=self.smtp_port,
                username=self.smtp_username,
                password=self.smtp_password,
                start_tls=True,
            )
            self.notification.send_status = NotificationSendStatus.SENT
            self.logger.info(
                f"Уведомление успешно отправлено на {self.notification.email}"  # noqa: E501
            )
        except Exception as e:
            self.logger.error(f"Ошибка при отправке уведомления: {e}")
            self.notification.send_status = NotificationSendStatus.FAILED
