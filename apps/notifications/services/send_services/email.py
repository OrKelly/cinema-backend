from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Callable, TypeVar

import aiosmtplib
from jinja2 import Environment, FileSystemLoader

from apps.notifications.services.send_services.base import (
    BaseNotificationService,
)
from core.config import config
from core.enums.notifications import (
    NotificationKindEnum,
    NotificationSendStatus,
)

HTMLTemplate = TypeVar("HTMLTemplate")
RenderedTemplate = TypeVar("RenderedTemplate")


@dataclass
class EmailNotificationService(BaseNotificationService):
    server = config.SMTP_SERVER
    port = config.SMTP_PORT
    username = config.SMTP_USERNAME
    password = config.SMTP_PASSWORD
    template_folder = Path(__file__).resolve().parents[4] / "templates"
    _template_to_kind = {
        NotificationKindEnum.EMPLOYEE_GREETING: "onboadring.html",
        NotificationKindEnum.CLIENT_GREETING: "welcome.html",
    }

    async def _validate(self, errors: dict[list]):
        if self.notification.send_status == NotificationSendStatus.SENT:
            errors["notification_already_sent"] = (
                "Уведомление уже было отправлено"
            )

    async def _notify(self, notification_data: dict) -> None:
        env = Environment(loader=FileSystemLoader(self.template_folder))

        template = self._get_template(env)

        body = self._get_body(template)

        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = notification_data["email"]
        msg["Subject"] = notification_data["title"]

        msg.attach(MIMEText(body, "html"))

        try:
            await aiosmtplib.send(
                msg,
                hostname=self.server,
                port=self.port,
                username=self.username,
                password=self.password,
                start_tls=True,
            )
            self.notification.send_status = NotificationSendStatus.SENT
            self.logger.info(
                f"Уведомление успешно отправлено на {notification_data['email']}"  # noqa: E501
            )
        except Exception as e:
            self.logger.error(f"Ошибка при отправке уведомления: {e}")
            self.notification.send_status = NotificationSendStatus.FAILED

    def _get_template(self, env: Environment) -> HTMLTemplate:
        return env.get_template(
            self._template_to_kind.get(self.notification.kind)
        )

    def _get_body(self, template: HTMLTemplate) -> RenderedTemplate:
        __body_methods: dict[NotificationKindEnum, Callable] = {
            NotificationKindEnum.EMPLOYEE_GREETING: self.__get_employee_greeting_body,  # noqa: E501
            NotificationKindEnum.CLIENT_GREETING: self.__get_client_greeting_body,  # noqa: E501
        }
        return template.render(**__body_methods.get(self.notification.kind)())

    def __get_employee_greeting_body(self) -> dict:
        return {
            "full_name": self.kwargs.get("full_name"),
            "email": self.kwargs.get("email"),
            "password": self.kwargs.get("password"),
        }

    def __get_client_greeting_body(self) -> dict:
        return {
            "full_name": self.kwargs.get("full_name"),
        }
