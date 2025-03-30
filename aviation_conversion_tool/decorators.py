"""Decorators"""
from typing import Callable

from qgis.PyQt.QtWidgets import (
    QMessageBox,
    QWidget
)

from .errors import AviationConversionBaseError


def show_dialog(msg: str) -> Callable:
    """Show dialog box when input is incorrect.

    :param msg: message to be displayed in dialog box.
    :return:
    """
    def dec_show_dialog(f):
        def wrapper_show_dialog(self):
            try:
                return f(self)
            except AviationConversionBaseError:
                QMessageBox.critical(QWidget(), "Message", msg)
            return None
        return wrapper_show_dialog
    return dec_show_dialog
