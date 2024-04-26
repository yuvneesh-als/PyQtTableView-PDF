from __future__ import annotations

from PySide2 import QtCore
from PySide2.QtGui import QBrush


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            return str(self._data.columns[section])
        elif orientation == QtCore.Qt.Vertical:
            return str(section)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])

        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter

        if role == QtCore.Qt.BackgroundRole:
            if index.row() in [2, 4]:
                return QBrush(QtCore.Qt.darkRed)
            if index.row() in [1, 7]:
                return QBrush(QtCore.Qt.darkYellow)

        if role == QtCore.Qt.ForegroundRole:
            if index.row() in [1, 7]:
                return QBrush(QtCore.Qt.white)
