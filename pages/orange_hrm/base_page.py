import time

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, expect,Dialog
class BasePage:
    def __init__(self, page):
        self.page = page

    # ----------------------
    # Low level waits
    # ----------------------
    def wait_for_element_to_locate(self, locator, timeout: int = 10000, retries: int = 2) -> bool:
        """
        Try to wait for given locator to be visible by retrying a few times.
        Returns True if located, False otherwise.
        """
        for attempt in range(retries):
            try:
                # Playwright Locator object expected as locator (string or Locator)
                loc = self.page.locator(locator) if isinstance(locator, str) else locator
                loc.wait_for(state="visible", timeout=timeout)
                # scroll into view if needed
                try:
                    loc.scroll_into_view_if_needed(timeout=timeout)
                except Exception:
                    pass
                return True
            except PlaywrightTimeoutError:
                print(f"Retrying... attempt {attempt + 1}")
                time.sleep(1)
                continue
            except Exception as e:
                print(f"Unexpected error : {e}")
                time.sleep(1)
                continue

        print("element not located within timeout.")
        return False

    def wait_for_element(self, locator, timeout: int = 10000):
        """
        Waits for the first visible element matching the locator on the main page.
        Returns the element (Locator) if found or raises TimeoutError.
        """
        end_time = time.time() + (timeout / 1000)
        loc = self.page.locator(locator)

        while time.time() < end_time:
            try:
                count = loc.count()
                for i in range(count):
                    el = loc.nth(i)
                    try:
                        el.wait_for(state="visible", timeout=500)
                        return el
                    except Exception:
                        continue
            except Exception:
                pass
            time.sleep(0.2)

        raise PlaywrightTimeoutError(f"No visible element found for locator '{locator}' on main page.")

    def wait_for_element_on_frame(self, frame_name: str, locator: str, timeout: int = 10000):
        """
        Waits for the first visible element matching the locator inside the given frame.
        Returns the element (Locator) if found or raises TimeoutError.
        """
        end_time = time.time() + (timeout / 1000)
        frame = self.page.frame(name=frame_name)
        if not frame:
            raise Exception(f"Frame '{frame_name}' not found.")

        loc = frame.locator(locator)

        while time.time() < end_time:
            try:
                count = loc.count()
                for i in range(count):
                    el = loc.nth(i)
                    try:
                        el.wait_for(state="visible", timeout=500)
                        return el
                    except Exception:
                        continue
            except Exception:
                pass
            time.sleep(0.2)

        raise PlaywrightTimeoutError(f"No visible element found for locator '{locator}' in frame '{frame_name}'.")

    # ----------------------
    # Locator helpers
    # ----------------------
    def get_locator(self, locator: str):
        """
        Waits for element and returns a Playwright Locator for the given locator on main page.
        """
        self.wait_for_element(locator)
        return self.page.locator(locator)

    def get_locator_on_frame(self, locator: str, frame_name: str):
        """
        Waits for element on frame and returns a Locator from the frame.
        """
        self.wait_for_element_on_frame(frame_name, locator)
        frame = self.page.frame(name=frame_name)
        return frame.locator(locator)

    # ----------------------
    # Click helpers
    # ----------------------
    def click(self, locator: str):
        self.wait_for_element(locator)
        loc = self.page.locator(locator)
        if self.wait_for_element_to_locate(loc):
            loc.click(force=True)
        else:
            raise Exception("Element not found .")

    def click_on_frame(self, locator: str, frame_name: str):
        self.wait_for_element_on_frame(frame_name, locator)
        frame = self.page.frame(name=frame_name)
        loc = frame.locator(locator)
        if self.wait_for_element_to_locate(loc):
            loc.click(force=True)
        else:
            raise Exception("Element not found .")

    def click_by_keyboard(self, locator: str, frame_name: str):
        """
        Focus on element inside frame and press Enter
        """
        self.wait_for_element_on_frame(frame_name, locator)
        frame = self.page.frame(name=frame_name)
        loc = frame.locator(locator)
        if self.wait_for_element_to_locate(loc):
            loc.focus()
            self.page.keyboard.press("Enter")
        else:
            raise Exception("Element not found .")

    def has_text_click(self, locator: str, text: str):
        """
        Click locator which has specific visible text
        """
        self.wait_for_element(locator)
        loc = self.page.locator(locator, has_text=f"{text}")
        if self.wait_for_element_to_locate(loc):
            loc.click()
        else:
            raise Exception("Element not found .")

    # ----------------------
    # Input helpers
    # ----------------------
    def fill_text(self, locator: str, value: str):
        self.wait_for_element(locator)
        loc = self.page.locator(locator)
        if self.wait_for_element_to_locate(loc):
            loc.fill(value, force=True)
        else:
            raise Exception("Element not found .")

    def fill_text_on_frame(self, locator: str, value: str, frame_name: str):
        self.wait_for_element_on_frame(frame_name, locator)
        frame = self.page.frame(name=frame_name)
        loc = frame.locator(locator)
        if self.wait_for_element_to_locate(loc):
            loc.fill(value)
        else:
            raise Exception("Element not found .")

    def type_text(self, locator: str, value: str):
        self.wait_for_element(locator)
        loc = self.page.locator(locator)
        if self.wait_for_element_to_locate(loc):
            loc.type(value)
        else:
            raise Exception("Element not found .")

    def set_input_files(self, locator: str, file):
        self.wait_for_element(locator)
        loc = self.page.locator(locator)
        if self.wait_for_element_to_locate(loc):
            loc.set_input_files(file)
        else:
            raise Exception("Element not found .")

    def set_input_files_on_frame(self, locator: str, file, frame_name: str):
        self.wait_for_element_on_frame(frame_name, locator)
        frame = self.page.frame(name=frame_name)
        loc = frame.locator(locator)
        if self.wait_for_element_to_locate(loc):
            loc.set_input_files(file)
        else:
            raise Exception("Element not found .")

    # ----------------------
    # Getters
    # ----------------------
    def get_inner_text(self, locator: str) -> str:
        self.wait_for_element(locator)
        loc = self.page.locator(locator)
        if self.wait_for_element_to_locate(loc):
            return loc.inner_text()
        else:
            raise Exception("Element not found .")

    def get_inner_text_on_frame(self, locator: str, frame_name: str, timeout: int = 10000) -> str:
        self.wait_for_element_on_frame(frame_name, locator, timeout=timeout)
        frame = self.page.frame(name=frame_name)
        loc = frame.locator(locator)
        if self.wait_for_element_to_locate(loc):
            return loc.inner_text()
        else:
            raise Exception("Element not found .")

    # ----------------------
    # Select helpers
    # ----------------------
    def select_option(self, locator: str, value):
        self.wait_for_element(locator)
        self.page.locator(locator).select_option(value)

    def select_option_on_frame(self, frame_name: str, locator: str, value):
        self.wait_for_element_on_frame(frame_name, locator)
        frame = self.page.frame(name=frame_name)
        loc = frame.locator(locator)
        if self.wait_for_element_to_locate(loc):
            loc.select_option(value)
        else:
            raise Exception("Element not found .")

    def is_visible(self, locator: str) -> bool:
        self.wait_for_element(locator)
        return self.page.locator(locator).is_visible()

    def select_dropdown_by_label(self, locator: str, visible_text: str):
        self.wait_for_element(locator)
        self.page.locator(locator).select_option(label=visible_text)

    # ----------------------
    # Alert / Dialog helpers
    # ----------------------
    def get_message_from_alert_without_frame(self, locator: str) -> str:
        alert_data = {"message": ""}

        def handle_alert(dialog: Dialog):
            alert_data["message"] = dialog.message
            dialog.accept()

        # attach handler and click
        self.page.on("dialog", handle_alert)
        self.click(locator)
        time.sleep(3)
        # remove handler to avoid side effects
        try:
            self.page.off("dialog", handle_alert)
        except Exception:
            pass
        return alert_data["message"]

    def get_message_from_alert(self, locator: str, value: str) -> str:
        alert_data = {"message": ""}

        def handle_alert(dialog: Dialog):
            alert_data["message"] = dialog.message
            dialog.accept()

        self.page.on("dialog", handle_alert)
        # click inside frame
        self.click_on_frame(locator, value)
        time.sleep(3)
        try:
            self.page.off("dialog", handle_alert)
        except Exception:
            pass
        return alert_data["message"]

    def get_message_from_alert_with_keyboard(self, locator: str, value: str) -> str:
        alert_data = {"message": ""}

        def handle_alert(dialog: Dialog):
            alert_data["message"] = dialog.message
            dialog.accept()

        self.page.on("dialog", handle_alert)
        # click by keyboard (press Enter) inside frame
        self.click_by_keyboard(locator, value)
        time.sleep(3)
        try:
            self.page.off("dialog", handle_alert)
        except Exception:
            pass
        return alert_data["message"]

    def accept_alert(self, locator: str):
        def handle_alert(dialog: Dialog):
            dialog.accept()

        self.page.on("dialog", handle_alert)
        self.click(locator)
        time.sleep(1)
        try:
            self.page.off("dialog", handle_alert)
        except Exception:
            pass

    # ----------------------
    # Popup removal helper (two popups sequence)
    # ----------------------
    def handle_remove_with_popups(self, remove_locator: str) -> str:
        """
        Clicks on the 'Remove' button, handles two popups:
         - First: confirmation (click OK)
         - Second: info alert (read message, click OK)
        Returns text from second popup.
        """
        popup_text = ""

        # Handle first popup - confirmation (auto accept)
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.wait_for_element(remove_locator)
        # Click on "Remove" button
        self.page.locator(remove_locator).click()

        # Handle second popup - get text, accept
        def second_popup(dialog: Dialog):
            nonlocal popup_text
            popup_text = dialog.message
            dialog.accept()

        self.page.once("dialog", second_popup)

        # Wait briefly to ensure popup appears
        try:
            # small wait - prefer explicit waits in tests, but this matches screenshot behavior
            self.page.wait_for_timeout(2000)
        except Exception:
            pass

        return popup_text

    # ----------------------
    # Multiple elements text getters
    # ----------------------
    def get_text_from_multiple_elements(self, locator: str):
        self.wait_for_element(locator)
        locator_obj = self.page.locator(locator)
        all_text = locator_obj.all_text_contents()
        return all_text

    def get_text_from_multiple_elements_on_frame(self, locator: str, frame_name: str):
        self.wait_for_element_on_frame(frame_name, locator)
        frame = self.page.frame(name=frame_name)
        locator_obj = frame.locator(locator)
        all_text = locator_obj.all_text_contents()
        return all_text

    # ----------------------
    # Window / new page helpers
    # ----------------------
    def switch_to_window(self, locator: str, timeout= 10000):
        """
        Click locator and wait for a new page to open; return the new page object/value.
        """
        context = self.page.context
        with context.expect_page(timeout=timeout) as new_page_info:
            self.click(locator)
        return new_page_info.value

    def switch_to_window_on_frame(self, locator: str, frame_name: str, timeout = 10000):
        """
        Click on element inside a frame which opens a new page; return the newly opened page.
        """
        context = self.page.context
        with context.expect_page(timeout=timeout) as new_page_info:
            self.click_on_frame(locator, frame_name)
        return new_page_info.value