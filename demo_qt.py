from __future__ import annotations

import sys

import pandas as pd
from PySide2 import QtWidgets
from PySide2.QtCore import QMarginsF
from PySide2.QtGui import QPageLayout, QPageSize
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWebEngineWidgets import QWebEnginePage

from builder import Builder
from model import TableModel

app = QtWidgets.QApplication(sys.argv)

data_model = TableModel(pd.read_csv("demo_data.csv"))

loader = QUiLoader()
window = loader.load(r"demo_ui.ui", None)
table = window.tableView.setModel(data_model)


def send_print_request():
    """
    Prepares the table view for printing
    """
    builder = Builder(data_model)
    builder.add_header("Demo PDF Report")
    builder.add_footer("Generated from PyQT TableView")
    html = builder.get_html()
    doc = QWebEnginePage()

    def print_pdf():
        """
        Prints the pdf
        """
        filename = "sample.pdf"

        layout = QPageLayout(QPageSize(QPageSize.A4),
                             QPageLayout.Portrait,
                             QMarginsF())

        doc.printToPdf(filename, layout)

    doc.loadFinished.connect(print_pdf)
    doc.setHtml(html)


window.button_print.clicked.connect(lambda: send_print_request())

window.show()
app.exec_()
