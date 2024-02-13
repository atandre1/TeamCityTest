from utils.datagenerator import DataGenerator

class ProjectData:
    @staticmethod
    def create_project_data():
        return {
            "parentProject": {
                "locator": "_Root"
            },
            "name": DataGenerator.fake_name(),
            "id": DataGenerator.fake_project_id(),
            "copyAllAssociatedSettings": True
        }
