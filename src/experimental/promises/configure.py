# -*- coding: utf-8 -*-
from venusianconfiguration import (
    configure,
    scan
)
from experimental.promises import (
    adapters,
    browser,
    transform
)

configure.i18n.registerTranslations(directory='locales')

scan(adapters)
scan(transform)
scan(browser)
