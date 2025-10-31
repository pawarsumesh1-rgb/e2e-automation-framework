import functools
import os
import time
import pytest
from datetime import datetime
from utils.logger import get_logger

logger = get_logger()

# ----------------------------------------------------------
# 📸 Decorator: Capture Screenshot on Failure
# ----------------------------------------------------------
def screenshot_on_failure(func):
    """
    Takes a screenshot if the test fails.
    Adds the screenshot as an attachment in Allure.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        page = None
        logout_obj = None

        # Try to get Playwright 'page' and 'logout_obj' from kwargs
        for obj in list(kwargs.values()):
            if hasattr(obj, "page"):
                page = getattr(obj, "page")
            if hasattr(obj, "logout"):
                logout_obj = obj

        try:
            return func(*args, **kwargs)
        except Exception as e:
            try:
                if page:
                    screenshots_path = os.path.join("target", "screenshots")
                    os.makedirs(screenshots_path, exist_ok=True)
                    screenshot_path = os.path.join(
                        screenshots_path,
                        f"{func._name}{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    )
                    page.screenshot(path=screenshot_path)
                    logger.info(f"Screenshot captured: {screenshot_path}")
                else:
                    print("⚠️ Page object not found for screenshot")
            except Exception as err:
                print(f"⚠️ Failed to capture screenshot due to error: {str(err)}")

            if not isinstance(e, AssertionError):
                logger.error(f"Testcase failed due to unexpected error: {str(e)}")
                pytest.fail(f"Testcase failed due to unexpected error: {str(e)}")
            raise
        finally:
            try:
                if logout_obj:
                    logout_obj.logout()
                    logger.info("✅ Logout successful")
            except Exception as err:
                logger.error(f"❌ Logout failed: {str(err)}")

    return wrapper


# ----------------------------------------------------------
# 🔁 Decorator: Retry on Failure
# ----------------------------------------------------------
def retry_on_failure(retries=2, delay=2):
    """
    Retries the decorated function if it fails.
    Adds retry count into function kwargs.
    """
    def decorator(func):
        func.retries = retries

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logout_obj = None
            for obj in list(kwargs.values()):
                if hasattr(obj, "logout"):
                    logout_obj = obj
                    break

            for attempt in range(1, retries + 1):
                try:
                    kwargs["retry_count"] = attempt
                    return func(*args, **kwargs)
                except AssertionError:
                    raise
                except Exception as e:
                    logger.warning(f"Attempt {attempt} failed with error: {e}")
                    if attempt == retries:
                        logger.error(f"Max retries reached ({retries}). Raising error.")
                        raise
                    else:
                        logger.info(f"Retrying after {delay} seconds...")
                        time.sleep(delay)
            try:
                if logout_obj:
                    logout_obj.logout()
                    logger.info("✅ Logout successful after retries")
            except Exception as err:
                logger.error(f"❌ Logout failed after retries: {err}")
        return wrapper
    return decorator


# ----------------------------------------------------------
# 🔁 Decorator: Retry for API Failures
# ----------------------------------------------------------
def retry_on_api_failure(max_retries=3, delay=2):
    """
    Retries API call functions on general exceptions.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except AssertionError:
                    raise
                except Exception as e:
                    logger.warning(f"API retry {attempt} failed: {str(e)}")
                    if attempt == max_retries:
                        logger.error(f"API call failed after {max_retries} retries.")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


# ----------------------------------------------------------
# 🕒 Decorator: Log Start and End of Test Function
# ----------------------------------------------------------
def log_start_end(func):
    """
    Logs the start and end of a test function for better traceability.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"🚀 STARTED: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            logger.info(f"✅ COMPLETED: {func.__name__}")
    return wrapper