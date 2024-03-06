from playwright.sync_api import sync_playwright


def test_e2e_create_project(project_data):
    project_data_1 = project_data()
    project_id = project_data_1.id
    project_name = project_data_1.name

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.set_viewport_size({"width": 1200, "height": 800})

    page.goto('http://localhost:8111/login.html')
    page.fill('#username', 'admin')
    page.fill('#password', 'admin')
    page.click('.loginButton')
    page.wait_for_url('http://localhost:8111/favorite/projects?mode=builds')

    page.goto('http://localhost:8111/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu')
    page.fill('#name', project_name)
    page.fill('#externalId', project_id)
    page.fill('#description', 'project description')
    page.click('#createProject')

    page.wait_for_url(f'http://localhost:8111/admin/editProject.html?projectId={project_id}')
    assert project_name in page.text_content('body')

