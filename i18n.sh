#!/bin/bash

bin/i18ndude rebuild-pot --pot src/experimental/futures/locales/experimental.futures.pot --merge src/experimental/futures/locales/manual.pot --create experimental.futures src/experimental/futures

bin/i18ndude sync --pot src/experimental/futures/locales/experimental.futures.pot src/experimental/futures/locales/*/LC_MESSAGES/experimental.futures.po
