import pytest
import requests

BASE_URL = 'http://admin:admin@localhost:8111'
class TestProjectCreate:

    def test_project_create(self):
        # Получение токена
        auth_response = requests.get(url = f"{BASE_URL}/authenticationTest.html?csrf)", auth=('admin', 'admin'))
        csrf_token = auth_response.text
        headers = {"X-TC-CSRF-Token": csrf_token}

        #Подготовка данных
        project_id ="simpleprojectID5"
        conf_id = "simpleconfID2"
        project_data={
                        "parentProject": {
                                    "locator": "_Root"
                                        },
                                    "name": "ProjectNameSimple5",
                                    "id": project_id,
                                    "copyAllAssociatedSettings": True
                        }
        build_data = {
            "id": conf_id,
            "name": "BuildConfName1",
            "project": {
                "id": project_id
            },
            "steps": {
                "step": [
                    {
                        "name": "myCommandLineStep",
                        "type": "simpleRunner",
                        "properties": {
                            "property": [
                                {
                                    "name": "script.content",
                                    "value": "echo 'Hello World!'"
                                },
                                {
                                    "name": "teamcity.step.mode",
                                    "value": "default"
                                },
                                {
                                    "name": "use.custom.script",
                                    "value": "true"
                                }
                            ]
                        }
                    }
                ]
            }
        }

        build_start_data = {
            "buildType": {
                "id": conf_id
            }
        }

        # Создание проекта
        create_responce = requests.post(url=f"{BASE_URL}/app/rest/projects", headers=headers, json=project_data)
        assert create_responce.status_code == 200, "Не удалось создать проект"

        check_project = requests.get(url=f"{BASE_URL}/app/rest/projects/id:{project_id}", headers=headers)
        assert check_project.status_code == 200, "Не удалось проверить проект"

        # Создание билда
        create_build_responce = requests.post(url=f"{BASE_URL}/app/rest/buildTypes", headers=headers, json=build_data)
        assert create_build_responce.status_code == 200, "Не удалось создать билд"

        # Запуск билда
        start_build_responce = requests.post(url=f"{BASE_URL}/app/rest/buildQueue", headers=headers, json=build_start_data)
        assert start_build_responce.status_code == 200, "Не удалось запустить билд"

        # Проверка статуса билда
        checkbuildstatus_responce = requests.get(url=f"{BASE_URL}/app/rest/buildQueue?locator=buildType(id:{conf_id})", headers=headers)
        assert checkbuildstatus_responce.status_code == 200, "Не удалось проверить билд"

        # Удаление проекта
        delete_project = requests.delete(url=f"{BASE_URL}/app/rest/projects/id:{project_id}", headers=headers)
        assert delete_project.status_code == 204, "Не удалось удалить проект"