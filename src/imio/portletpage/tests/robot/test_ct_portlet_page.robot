# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s imio.portletpage -t test_portlet_page.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src imio.portletpage.testing.IMIO_PORTLETPAGE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/imio/portletpage/tests/robot/test_portlet_page.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a PortletPage
  Given a logged-in site administrator
    and an add PortletPage form
   When I type 'My PortletPage' into the title field
    and I submit the form
   Then a PortletPage with the title 'My PortletPage' has been created

Scenario: As a site administrator I can view a PortletPage
  Given a logged-in site administrator
    and a PortletPage 'My PortletPage'
   When I go to the PortletPage view
   Then I can see the PortletPage title 'My PortletPage'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add PortletPage form
  Go To  ${PLONE_URL}/++add++PortletPage

a PortletPage 'My PortletPage'
  Create content  type=PortletPage  id=my-portlet_page  title=My PortletPage

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the PortletPage view
  Go To  ${PLONE_URL}/my-portlet_page
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a PortletPage with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the PortletPage title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
