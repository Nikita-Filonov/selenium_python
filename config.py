from pydantic import BaseModel

from utils.webdriver_factory.browser import Browser


class DriverConfig(BaseModel):
    browser: Browser = Browser.CHROME
    remote_url: str = ""
    wait_time: int = 10
    page_load_wait_time: int = 0
    options: list[str] = []
    capabilities: dict[str, str] = {}
    experimental_options: list[dict] | None = None
    seleniumwire_options: dict = {}
    extension_paths: list[str] | None = None
    webdriver_kwargs: dict | None = None
    version: str | None
    local_path: str = ""


class LoggingConfig(BaseModel):
    pylog_level: str = "INFO"
    screenshots_on: bool = True


class ViewportConfig(BaseModel):
    maximize: bool = True
    width: int = 1440
    height: int = 900
    orientation: str = "portrait"


class UIConfig(BaseModel):
    base_url: str = 'https://www.w3schools.com'
    driver: DriverConfig = DriverConfig()
    logging: LoggingConfig = LoggingConfig()
    viewport: ViewportConfig = ViewportConfig()
    custom: dict = {}
