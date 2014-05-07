# bin/robot-server experimental.futures.testing.PROMISES_ROBOT_TESTING
# bin/robot src/experimental/futures/tests/acceptance/test_installed.robot

*** Settings ***

Resource  futures.robot

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Test Cases ***

Plone is installed
    Go to  ${PLONE_URL}
    Page should contain  Powered by Plone
