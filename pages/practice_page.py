from typing import List, Optional, Tuple

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class PracticePage(BasePage):

    # ── Radio Buttons ────────────────────────────────────────────────────────
    _RADIO: dict = {
        1: (By.CSS_SELECTOR, "input[value='radio1']"),
        2: (By.CSS_SELECTOR, "input[value='radio2']"),
        3: (By.CSS_SELECTOR, "input[value='radio3']"),
    }

    # ── Dropdown ─────────────────────────────────────────────────────────────
    _DROPDOWN: Tuple = (By.ID, "dropdown-class-example")

    # ── Checkboxes ───────────────────────────────────────────────────────────
    _CHECKBOX: dict = {
        1: (By.ID, "checkBoxOption1"),
        2: (By.ID, "checkBoxOption2"),
        3: (By.ID, "checkBoxOption3"),
    }

    # ── Autocomplete ─────────────────────────────────────────────────────────
    _AUTOCOMPLETE_INPUT: Tuple = (By.ID, "autocomplete")
    _AUTOCOMPLETE_OPTIONS: Tuple = (
        By.CSS_SELECTOR,
        "ul.ui-autocomplete li.ui-menu-item",
    )

    # ── Window / Tab ─────────────────────────────────────────────────────────
    _OPEN_WINDOW_BTN: Tuple = (By.ID, "openwindow")
    _OPEN_TAB_LINK: Tuple = (By.ID, "opentab")

    # ── Alerts ───────────────────────────────────────────────────────────────
    _ALERT_BTN: Tuple = (By.ID, "alertbtn")
    _CONFIRM_BTN: Tuple = (By.ID, "confirmbtn")

    # ── Mouse Hover ──────────────────────────────────────────────────────────
    _MOUSE_HOVER: Tuple = (By.ID, "mousehover")
    _HOVER_TOP: Tuple = (By.CSS_SELECTOR, "a[href='#top']")
    _HOVER_RELOAD: Tuple = (By.LINK_TEXT, "Reload")

    # ── Element Display ──────────────────────────────────────────────────────
    _HIDE_BTN: Tuple = (By.ID, "hide-textbox")
    _SHOW_BTN: Tuple = (By.ID, "show-textbox")
    _DISPLAYED_ELEMENT: Tuple = (By.ID, "displayed-text")

    # ── Web Table 1 – Course List ─────────────────────────────────────────────
    # 10-row table: Instructor | Course Title | Price
    _COURSE_TABLE_ROWS: Tuple = (By.XPATH, "//table[@name='courses']//tbody/tr[td]")

    # ── Web Table 2 – Fixed Header ────────────────────────────────────────────
    # Personnel table with footer row showing the collected total.
    _FIXED_TABLE_BODY_ROWS: Tuple = (
        By.CSS_SELECTOR,
        "div.tableFixHead table tbody tr",
    )
    _FIXED_TABLE_TOTAL_ROW: Tuple = (By.XPATH, "//div[@class='totalAmount']")

    # ── iFrame ───────────────────────────────────────────────────────────────
    _IFRAME: Tuple = (By.ID, "courses-iframe")

    # =========================================================================
    # Radio Button Methods
    # =========================================================================

    def select_radio(self, option: int) -> None:
        self.click(self._RADIO[option])

    def is_radio_selected(self, option: int) -> bool:
        return self.find_element(self._RADIO[option]).is_selected()

    # =========================================================================
    # Dropdown Methods
    # =========================================================================

    def select_dropdown(self, visible_text: str) -> None:
        Select(self.find_element(self._DROPDOWN)).select_by_visible_text(visible_text)

    def get_selected_dropdown_option(self) -> str:
        return Select(self.find_element(self._DROPDOWN)).first_selected_option.text

    # =========================================================================
    # Checkbox Methods
    # =========================================================================

    def check_option(self, option: int) -> None:
        element = self.find_element(self._CHECKBOX[option])
        if not element.is_selected():
            element.click()

    def uncheck_option(self, option: int) -> None:
        element = self.find_element(self._CHECKBOX[option])
        if element.is_selected():
            element.click()

    def is_option_checked(self, option: int) -> bool:
        return self.find_element(self._CHECKBOX[option]).is_selected()

    # =========================================================================
    # Autocomplete Methods
    # =========================================================================

    def type_autocomplete(self, text: str) -> None:
        self.send_keys(self._AUTOCOMPLETE_INPUT, text)

    def get_suggestions(self) -> List[str]:
        return [opt.text for opt in self.find_elements(self._AUTOCOMPLETE_OPTIONS)]

    def select_suggestion(self, text: str) -> None:
        for opt in self.find_elements(self._AUTOCOMPLETE_OPTIONS):
            if opt.text.strip() == text:
                opt.click()
                return
        raise ValueError(f"Suggestion '{text}' not found in autocomplete list")

    def get_autocomplete_value(self) -> str:
        return self.find_element(self._AUTOCOMPLETE_INPUT).get_attribute("value")

    # =========================================================================
    # Window / Tab Methods
    # =========================================================================

    def click_open_window(self) -> None:
        self.click(self._OPEN_WINDOW_BTN)

    def click_open_tab(self) -> None:
        self.click(self._OPEN_TAB_LINK)

    def switch_to_new_window(self, original_handle: str) -> str:
        """Switch to the first window handle that is not *original_handle*."""
        for handle in self.driver.window_handles:
            if handle != original_handle:
                self.driver.switch_to.window(handle)
                return handle
        raise RuntimeError("No new window or tab was opened")

    def close_and_switch_back(self, original_handle: str) -> None:
        self.driver.close()
        self.driver.switch_to.window(original_handle)

    # =========================================================================
    # Alert Methods
    # =========================================================================

    def click_alert_button(self) -> None:
        self.click(self._ALERT_BTN)

    def click_confirm_button(self) -> None:
        self.click(self._CONFIRM_BTN)

    # =========================================================================
    # Mouse Hover Methods
    # =========================================================================

    def hover_mouse_element(self) -> None:
        element = self.find_element(self._MOUSE_HOVER)
        ActionChains(self.driver).move_to_element(element).perform()

    def click_hover_top(self) -> None:
        self.click(self._HOVER_TOP)

    def click_hover_reload(self) -> None:
        self.click(self._HOVER_RELOAD)

    # =========================================================================
    # Element Display Methods
    # =========================================================================

    def click_show_hide(self) -> None:
        self.click(self._HIDE_BTN)

    def click_show_show(self) -> None:
        self.click(self._SHOW_BTN)

    def is_displayed_element_visible(self) -> bool:
        return self.is_element_visible(self._DISPLAYED_ELEMENT)

    # =========================================================================
    # Web Table 1 – Course List
    # =========================================================================

    def get_all_courses(self) -> List[tuple]:
        """Return list of (instructor, course_title, price) for every data row."""
        rows = self.find_elements(self._COURSE_TABLE_ROWS)
        result = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 3:
                result.append((cells[0].text, cells[1].text, cells[2].text))
        return result

    def get_course_price(self, course_name: str) -> Optional[str]:
        """Return the price column value for the first row whose title matches."""
        for instructor, title, price in self.get_all_courses():
            if course_name.lower() in title.lower():
                return price
        return None

    # =========================================================================
    # Web Table 2 – Fixed Header
    # =========================================================================

    def get_fixed_table_rows(self) -> List[tuple]:
        """Return list of (name, position, city, amount) for each body row."""
        rows = self.find_elements(self._FIXED_TABLE_BODY_ROWS)
        result = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 4:
                result.append(
                    (cells[0].text, cells[1].text, cells[2].text, cells[3].text)
                )
        return result

    def get_total_amount(self) -> str:
        text = self.get_text(self._FIXED_TABLE_TOTAL_ROW)
        return text.split(":")[-1].strip()

    def get_person_amount(self, name: str) -> Optional[str]:
        for row_name, _, _, amount in self.get_fixed_table_rows():
            if row_name.strip() == name:
                return amount
        return None

    # =========================================================================
    # iFrame Methods
    # =========================================================================

    def switch_to_iframe(self) -> None:
        iframe = self.find_element(self._IFRAME)
        self.driver.switch_to.frame(iframe)

    def switch_to_default_content(self) -> None:
        self.driver.switch_to.default_content()

    def get_iframe_links(self) -> List[str]:
        """Must be called after switch_to_iframe()."""
        links = self.driver.find_elements(By.TAG_NAME, "a")
        return [link.text for link in links if link.text.strip()]
