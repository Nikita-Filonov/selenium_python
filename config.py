from pydantic import BaseModel, BaseSettings, Field

from utils.webdriver.factory.browser import Browser


class DriverConfig(BaseSettings):
    browser: Browser = Field(default=Browser.CHROME, env="BROWSER")
    remote_url: str = Field(default="", env="REMOTE_URL")
    wait_time: int = 10
    page_load_wait_time: int = 0
    options: list[str] = [
        "ignore-certificate-errors",
        "--no-sandbox",
        "disable-infobars",
        '--headless',
        '--disable-extensions',
        '--disable-gpu'
    ]
    capabilities: dict[str, str] = {}
    experimental_options: list[dict] | None = None
    seleniumwire_options: dict = {}
    extension_paths: list[str] | None = None
    webdriver_kwargs: dict | None = None
    version: str | None
    local_path: str = ""

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class LoggingConfig(BaseSettings):
    log_level: str = "INFO"
    screenshots_on: bool = Field(default=True, env="SCREENSHOTS_ON")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class ViewportConfig(BaseModel):
    maximize: bool = True
    width: int = 1440
    height: int = 900
    orientation: str = "portrait"


class UIConfig(BaseSettings):
    base_url: str = Field(env="BASE_URL")
    driver: DriverConfig = DriverConfig()
    logging: LoggingConfig = LoggingConfig()
    viewport: ViewportConfig = ViewportConfig()
    custom: dict = {}

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
