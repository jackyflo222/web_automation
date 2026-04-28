"""
Test suite for https://rahulshettyacademy.com/AutomationPractice/
Each test class maps to one UI section of the page.
"""
import pytest
from pages.practice_page import PracticePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ---------------------------------------------------------------------------
# Shared page fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def page(driver):
    return PracticePage(driver)


# ---------------------------------------------------------------------------
# Radio Buttons
# ---------------------------------------------------------------------------

@pytest.mark.radio
class TestRadioButtons:

    def test_select_radio1_is_checked(self, page):
        page.select_radio(1)
        assert page.is_radio_selected(1)

    def test_select_radio2_is_checked(self, page):
        page.select_radio(2)
        assert page.is_radio_selected(2)

    def test_select_radio3_is_checked(self, page):
        page.select_radio(3)
        assert page.is_radio_selected(3)

    def test_radio_selection_is_exclusive(self, page):
        page.select_radio(1)
        page.select_radio(3)
        assert page.is_radio_selected(3)
        assert not page.is_radio_selected(1)


# ---------------------------------------------------------------------------
# Dropdown
# ---------------------------------------------------------------------------

@pytest.mark.dropdown
class TestDropdown:

    def test_select_option1(self, page):
        page.select_dropdown("Option1")
        assert page.get_selected_dropdown_option() == "Option1"

    def test_select_option2(self, page):
        page.select_dropdown("Option2")
        assert page.get_selected_dropdown_option() == "Option2"

    def test_select_option3(self, page):
        page.select_dropdown("Option3")
        assert page.get_selected_dropdown_option() == "Option3"

    def test_dropdown_option_changes(self, page):
        page.select_dropdown("Option1")
        page.select_dropdown("Option3")
        assert page.get_selected_dropdown_option() == "Option3"


# ---------------------------------------------------------------------------
# Checkboxes
# ---------------------------------------------------------------------------

@pytest.mark.checkbox
class TestCheckboxes:

    def test_check_option1(self, page):
        page.check_option(1)
        assert page.is_option_checked(1)

    def test_check_all_options(self, page):
        for opt in (1, 2, 3):
            page.check_option(opt)
        assert all(page.is_option_checked(o) for o in (1, 2, 3))

    def test_uncheck_option(self, page):
        page.check_option(2)
        page.uncheck_option(2)
        assert not page.is_option_checked(2)

    def test_check_and_uncheck_individually(self, page):
        page.check_option(1)
        page.check_option(3)
        page.uncheck_option(1)
        assert not page.is_option_checked(1)
        assert page.is_option_checked(3)


# ---------------------------------------------------------------------------
# Autocomplete / Suggestion
# ---------------------------------------------------------------------------

@pytest.mark.autocomplete
class TestAutocomplete:

    def test_suggestions_appear_on_input(self, page):
        page.type_autocomplete("Ind")
        suggestions = page.get_suggestions()
        assert len(suggestions) > 0

    def test_suggestions_match_typed_text(self, page):
        page.type_autocomplete("Ind")
        suggestions = page.get_suggestions()
        assert all("Ind" in s for s in suggestions)

    def test_select_india_from_suggestions(self, page):
        page.type_autocomplete("Ind")
        page.select_suggestion("India")
        assert page.get_autocomplete_value() == "India"

    def test_select_indonesia_from_suggestions(self, page):
        page.type_autocomplete("Ind")
        page.select_suggestion("Indonesia")
        assert page.get_autocomplete_value() == "Indonesia"


# ---------------------------------------------------------------------------
# Open Window
# ---------------------------------------------------------------------------

@pytest.mark.windows
class TestOpenWindow:

    def test_new_window_opens(self, driver, page):
        original = driver.current_window_handle
        page.click_open_window()
        page.switch_to_new_window(original)
        assert driver.current_window_handle != original

    def test_new_window_has_different_url(self, driver, page):
        original = driver.current_window_handle
        original_url = driver.current_url
        page.click_open_window()
        page.switch_to_new_window(original)
        assert driver.current_url != original_url

    def test_can_close_new_window_and_return(self, driver, page):
        original = driver.current_window_handle
        page.click_open_window()
        page.switch_to_new_window(original)
        page.close_and_switch_back(original)
        assert driver.current_window_handle == original
        assert len(driver.window_handles) == 1


# ---------------------------------------------------------------------------
# Open Tab
# ---------------------------------------------------------------------------

@pytest.mark.windows
class TestOpenTab:

    def test_new_tab_opens(self, driver, page):
        original = driver.current_window_handle
        page.click_open_tab()
        page.switch_to_new_window(original)
        assert driver.current_window_handle != original

    def test_new_tab_url_is_qaclickacademy(self, driver, page):
        original = driver.current_window_handle
        page.click_open_tab()
        page.switch_to_new_window(original)
        assert "qaclickacademy" in driver.current_url.lower()

    def test_can_close_tab_and_return(self, driver, page):
        original = driver.current_window_handle
        page.click_open_tab()
        page.switch_to_new_window(original)
        page.close_and_switch_back(original)
        assert driver.current_window_handle == original


# ---------------------------------------------------------------------------
# Alerts
# ---------------------------------------------------------------------------

@pytest.mark.alerts
class TestAlerts:

    def test_alert_is_present_after_click(self, page):
        page.click_alert_button()
        text = page.accept_alert()
        assert text is not None and len(text) > 0

    def test_confirm_dialog_accept(self, page):
        page.click_confirm_button()
        text = page.accept_alert()
        assert text is not None and len(text) > 0

    def test_confirm_dialog_dismiss(self, page):
        page.click_confirm_button()
        text = page.dismiss_alert()
        assert text is not None and len(text) > 0


# ---------------------------------------------------------------------------
# Mouse Hover
# ---------------------------------------------------------------------------

@pytest.mark.hover
class TestMouseHover:

    def test_top_link_visible_after_hover(self, driver, page):
        page.hover_mouse_element()
        top_link = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Top"))
        )
        assert top_link.is_displayed()

    def test_reload_link_visible_after_hover(self, driver, page):
        page.hover_mouse_element()
        reload_link = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Reload"))
        )
        assert reload_link.is_displayed()

    def test_click_top_link(self, page):
        page.hover_mouse_element()
        page.click_hover_top()

    def test_click_reload_link(self, driver, page):
        original_url = driver.current_url
        page.hover_mouse_element()
        page.click_hover_reload()
        assert driver.current_url == original_url


# ---------------------------------------------------------------------------
# Web Table – Course List
# ---------------------------------------------------------------------------

@pytest.mark.tables
class TestCourseTable:

    def test_table_has_ten_courses(self, page):
        courses = page.get_all_courses()
        assert len(courses) == 10

    def test_all_rows_have_three_columns(self, page):
        courses = page.get_all_courses()
        assert all(len(row) == 3 for row in courses)

    def test_selenium_course_exists(self, page):
        price = page.get_course_price("Selenium")
        assert price is not None

    def test_all_prices_are_non_empty(self, page):
        courses = page.get_all_courses()
        assert all(row[2].strip() for row in courses)


# ---------------------------------------------------------------------------
# Web Table – Fixed Header
# ---------------------------------------------------------------------------

@pytest.mark.tables
class TestFixedHeaderTable:

    def test_table_has_nine_data_rows(self, page):
        rows = page.get_fixed_table_rows()
        assert len(rows) == 9

    def test_total_amount_is_296(self, page):
        total = page.get_total_amount()
        assert "296" in total

    def test_all_rows_have_four_columns(self, page):
        rows = page.get_fixed_table_rows()
        assert all(len(row) == 4 for row in rows)

    def test_specific_person_amount(self, page):
        # Alex is listed in the personnel table
        amount = page.get_person_amount("Alex")
        assert amount is not None


# ---------------------------------------------------------------------------
# iFrame
# ---------------------------------------------------------------------------

@pytest.mark.iframe
class TestIFrame:

    def test_can_switch_to_iframe(self, page):
        page.switch_to_iframe()
        # If we got here without an exception the switch succeeded.
        page.switch_to_default_content()

    def test_iframe_contains_links(self, page):
        page.switch_to_iframe()
        links = page.get_iframe_links()
        assert len(links) > 0
        page.switch_to_default_content()

    def test_can_return_to_main_content(self, driver, page):
        page.switch_to_iframe()
        page.switch_to_default_content()
        # Verify we can still find the main-page autocomplete input
        from selenium.webdriver.common.by import By
        assert driver.find_element(By.ID, "autocomplete")


# ---------------------------------------------------------------------------
# Element Visibility (Show / Hide)
# ---------------------------------------------------------------------------

@pytest.mark.visibility
class TestElementVisibility:

    def test_element_is_visible_by_default(self, page):
        assert page.is_displayed_element_visible()

    def test_element_hidden_after_clicking_hide(self, page):
        page.click_show_hide()
        assert not page.is_displayed_element_visible()

    def test_element_visible_again_after_clicking_show(self, page):
        page.click_show_hide()   # hide
        page.click_show_show()   # show again
        assert page.is_displayed_element_visible()
