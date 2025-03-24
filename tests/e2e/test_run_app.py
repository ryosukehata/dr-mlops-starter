# Copyright 2024 DataRobot, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from tests.e2e.utils import (
    wait_for_element_to_be_clickable,
    wait_for_element_to_be_visible,
)


@pytest.mark.usefixtures("check_if_logged_in")
def test_app_loaded(browser: webdriver.Chrome, get_app_url: str) -> None:
    browser.get(get_app_url)
    assert wait_for_element_to_be_visible(
        browser,
        By.XPATH,
        "//p[contains(text(), 'Select the deployment and scoring dataset to use:')]",
    )


@pytest.mark.usefixtures("check_if_logged_in")
def test_make_predictions(browser: webdriver.Chrome):
    submit_btn = "[data-testid='stBaseButton-secondaryFormSubmit']"

    wait_for_element_to_be_clickable(browser, By.CSS_SELECTOR, submit_btn)
    browser.find_element(By.CSS_SELECTOR, submit_btn).click()

    assert wait_for_element_to_be_visible(
        browser, By.CSS_SELECTOR, "[data-testid='data-grid-canvas']", timeout=60
    )
