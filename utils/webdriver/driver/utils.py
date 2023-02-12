import os

import allure

from config import get_ui_config
from utils.webdriver.driver.page import Page


def attach_screenshot(page: Page, test_name: str):
    ui_config = get_ui_config()

    if not os.path.exists(ui_config.logging.screenshots_dir):
        os.mkdir(ui_config.logging.screenshots_dir)

    screenshot = page.screenshot(f'screenshots/{test_name}.png')

    allure.attach.file(
        screenshot, name='Page', attachment_type=allure.attachment_type.PNG
    )
