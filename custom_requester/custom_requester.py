from http import HTTPStatus

from enums.host import BASE_URL


class CustomRequester:
    base_headers = dict({"Content-Type": "application/json", "Accept": "application/json"})

    def __init__(self, session):
        self.session = session
        self.base_url = BASE_URL

    def send_request(self, method, endpoint, data=None, expected_status=HTTPStatus.OK):
        """
        Враппер для запросов. Позволяет прикручивать дополнительную логику
        :param method: Метод запроса
        :param endpoint: Эндпоинт для склейки с BASE_URL
        :param data: Тело запроса. По умолчанию пустое, чтобы пропускало nocontent запросы
        :param expected_status: Ожидаемый статус код
        :return: Возвращает объект ответа
        """
        url=f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, json=data)
        if response.status_code !=expected_status:
            raise ValueError(f"Unexpected status code: {response.status_code}")
        return response

    def _update_session_headers(self, **kwargs):
        self.headers=self.base_headers.copy()
        self.headers.update(kwargs)
        self.session.headers.update(self.headers)