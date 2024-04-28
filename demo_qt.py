from __future__ import annotations

import sys

import pandas as pd
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader


from builder import Builder
from model import TableModel

app = QtWidgets.QApplication(sys.argv)

data_model = TableModel(pd.read_csv("demo_data.csv"))

loader = QUiLoader()
window = loader.load(r"demo_ui.ui", None)
table = window.tableView.setModel(data_model)


def print_pdf():
    """
    Prints the table view
    """
    builder = Builder(data_model)
    builder.add_header("Demo PDF Report")
    builder.add_footer("Generated from PyQT TableView")
    builder.print_pdf("demo_report.pdf")


window.button_print.clicked.connect(lambda: print_pdf())

window.show()
app.exec_()
