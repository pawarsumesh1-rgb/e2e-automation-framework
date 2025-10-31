from collections import OrderedDict
import json
import allure
from typing import Union, Mapping

class UIClient:
    """
    Utility class to attach UI-related data (element locators / attributes)
    to test reports (Allure) in a pretty JSON format.
    """

    @staticmethod
    def attach_ui_data(page_name: str, odict: Union[Mapping, OrderedDict]):
        """
        Attach UI element data to Allure report.

        :param page_name: Name of the page on screen (used in the attachment name)
        :param odict: OrderedDict (or mapping) of UI elements and their data
        """
        # Ensure we have an OrderedDict so ordering is preserved if required
        if not isinstance(odict, OrderedDict):
            try:
                odict = OrderedDict(odict)
            except Exception:
                # Fall back to creating OrderedDict from items if odict is e.g. a generator
                odict = OrderedDict(list(odict.items()) if hasattr(odict, "items") else odict)

        # Convert to pretty JSON string with indentation
        pretty_dict = json.dumps(odict, indent=4, ensure_ascii=False)

        # Attach to Allure with a descriptive name and JSON content type
        try:
            allure.attach(
                pretty_dict,
                name=f"Page Data - {page_name}",
                attachment_type=allure.attachment_type.JSON
            )
        except Exception as e:
            # If Allure isn't available (e.g., running outside pytest/allure), print fallback
            print(f"[UIClient] Could not attach to Allure: {e}\nData:\n{pretty_dict}")