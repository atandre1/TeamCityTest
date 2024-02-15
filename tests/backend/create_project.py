import pytest
import requests

from custom_requester.custom_requester import CustomRequester
from data.project_data import ProjectData

BASE_URL = 'http://admin:admin@localhost:8111'


class CustomRequestor:
    pass


class TestProjectCreate:
    project_data = None

    @classmethod
    def setup_class(cls):
        cls.project_data = ProjectData.create_project_data()
        cls.create_project_id = cls.project_data["id"]

    def test_project_create(self):
        requester = CustomRequester(requests.Session())
        requester.session.auth = ("admin", "admin")

        # requester=CustomRequester(requests.Session())
        # # Получение токена
        # auth_response = requests.get(url = f"{BASE_URL}/authenticationTest.html?csrf)", auth=('admin', 'admin'))
        # csrf_token = auth_response.text
        # headers = {"X-TC-CSRF-Token": csrf_token}
        #
        # #Подготовка данных
        # project_id ="simpleprojectID5"
        # conf_id = "simpleconfID2"
        # project_data={
        #     "parentProject": {
        #         "locator": "_Root"
        #     },
        #     "name": "ProjectNameSimple5",
        #     "id": project_id,
        #     "copyAllAssociatedSettings": True
        # }
        # build_data = {
        #     "id": conf_id,
        #     "name": "BuildConfName1",
        #     "project": {
        #         "id": project_id
        #     },
        #     "steps": {
        #         "step": [
        #             {
        #                 "name": "myCommandLineStep",
        #                 "type": "simpleRunner",
        #                 "properties": {
        #                     "property": [
        #                         {
        #                             "name": "script.content",
        #                             "value": "echo 'Hello World!'"
        #                         },
        #                         {
        #                             "name": "teamcity.step.mode",
        #                             "value": "default"
        #                         },
        #                         {
        #                             "name": "use.custom.script",
        #                             "value": "true"
        #                         }
        #                     ]
        #                 }
        #             }
        #         ]
        #     }
        # }


        # Получение токена
        csrf_token = requester.send_request("GET", "/authenticationTest.html?csrf").text
        requester._update_session_headers(**{"X-TC-CSRF-Token": csrf_token})

        # Создание проекта
        create_responce = requester.send_request("POST", "/app/rest/projects", data=self.project_data)
        assert create_responce.status_code == 200, "Не удалось создать проект"

        check_project = requester.send_request("GET", f"/app/rest/projects/id:{self.create_project_id}")
        assert check_project.status_code == 200, "Не удалось проверить проект"

        # # Создание билда
        # create_build_responce = requests.post(url=f"{BASE_URL}/app/rest/buildTypes", headers=headers, json=build_data)
        # assert create_build_responce.status_code == 200, "Не удалось создать билд"
        #
        # # Запуск билда
        # start_build_responce = requests.post(url=f"{BASE_URL}/app/rest/buildQueue", headers=headers, json=build_start_data)
        # assert start_build_responce.status_code == 200, "Не удалось запустить билд"
        #
        # # Проверка статуса билда
        # checkbuildstatus_responce = requests.get(url=f"{BASE_URL}/app/rest/buildQueue?locator=buildType(id:{conf_id})", headers=headers)
        # assert checkbuildstatus_responce.status_code == 200, "Не удалось проверить билд"

        # Удаление проекта
        delete_project = requester.send_request("DELETE", f"/app/rest/projects/id:{self.create_project_id}", expected_status=204)
        assert delete_project.status_code == 204, "Не удалось удалить проект"

