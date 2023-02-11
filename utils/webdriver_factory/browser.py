from enum import Enum


class Browser(str, Enum):
    CHROME = "chrome"
    EDGE = "edge"
    FIREFOX = "firefox"
    IE = "ie"
    OPERA = "opera"
