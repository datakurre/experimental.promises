#!/bin/bash

bin/i18ndude rebuild-pot --pot src/experimental/promises/locales/experimental.promises.pot --merge src/experimental/promises/locales/manual.pot --create experimental.promises src/experimental/promises

bin/i18ndude sync --pot src/experimental/promises/locales/experimental.promises.pot src/experimental/promises/locales/*/LC_MESSAGES/experimental.promises.po
