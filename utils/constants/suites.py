from enum import Enum


class Suite(str, Enum):
    SANITY = 'Sanity'
    SMOKE = 'Smoke'
    CORE_REGRESSION = 'Core Regression',
    EXTENDED_REGRESSION = 'Extended Regression'
