# -*- coding: utf-8 -*-

"""
gspread.exceptions
~~~~~~~~~~~~~~~~~~

Exceptions used in gspread.

"""


class GSpreadException(Exception):
    """A base class for gspread's exceptions."""


class SpreadsheetNotFound(GSpreadException):
    """Trying to open non-existent or inaccessible spreadsheet."""


class WorksheetNotFound(GSpreadException):
    """Trying to open non-existent or inaccessible worksheet."""


class CellNotFound(GSpreadException):
    """Cell lookup exception."""


class NoValidUrlKeyFound(GSpreadException):
    """No valid key found in URL."""


class IncorrectCellLabel(GSpreadException):
    """The cell label is incorrect."""


class APIError(GSpreadException):
    def __init__(self, response):

        super(APIError, self).__init__(self._extract_text(response))

    def _extract_text(self, response):
        return self._text_from_detail(response) or response.text

    def _text_from_detail(self, response):
        try:
            errors = response.json()["error"]
            self.return_code = int(errors["code"])
            self.message = errors["message"]

            # The detailed section "errors" is only here on errors from google drive API,
            # not in errors from google spreadsheet API
            self.details = errors.get("errors") or ""

            return "({}) - {}".format(self.return_code, self.message)
        except (AttributeError, KeyError, ValueError):
            return None
