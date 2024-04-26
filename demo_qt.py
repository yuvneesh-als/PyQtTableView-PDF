from __future__ import annotations

import sys

import pandas as pd
from PySide2 import QtCore, QtWidgets
from PySide2.QtUiTools import QUiLoader

from model import TableModel

app = QtWidgets.QApplication(sys.argv)

data_model = TableModel(pd.read_csv("demo_data.csv"))

loader = QUiLoader()
window = loader.load(r"demo_ui.ui", None)

table = window.tableView.setModel(data_model)


window.show()
app.exec_()
