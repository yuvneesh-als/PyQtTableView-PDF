from __future__ import annotations

from xhtml2pdf import pisa
import pandas as pd
from PySide2 import QtCore, QtGui
from model import TableModel


class StyleBuilder:
    """
    Handles creating the css by using QBrush properties
    """
    def __init__(self):
        self.background_color = ""
        self.foreground_color = ""

    def add_color(self, category, color):
        """
        Adds a color of the given category i.e. background, foreground
        """

        if not color:
            return ""
        if category == "bg":
            self.background_color = color
        elif category == "fg":
            self.foreground_color = color

    def get_style(self) -> str:
        """
        Build the css string using the attributes

        Returns:
            css string
        """
        txt = 'style="'
        if self.background_color:
            txt += f"background-color:{self.background_color};"
        if self.foreground_color:
            txt += f"color:{self.foreground_color};"
        txt += '"'

        if txt != 'style=""':
            return txt
        else:
            return ""


class TableBuilder:
    """
    Manages creating html for a PyQt Sample Model
    """
    def __init__(self, data_model):
        self.model = data_model

    def _build_style(self, row: int, column: int) -> str:
        """
        Creates inline css for a given cell

        Returns:
            css as a string
        """
        style_builder = StyleBuilder()

        background_brush: QtGui.QBrush = self.model.data(self.model.index(row, column), role=QtCore.Qt.BackgroundRole)
        foreground_brush: QtGui.QBrush = self.model.data(self.model.index(row, column), role=QtCore.Qt.ForegroundRole)

        if background_brush:
            style_builder.add_color("bg", background_brush.color().name())
        if foreground_brush:
            style_builder.add_color("fg", foreground_brush.color().name())

        return style_builder.get_style()

    def _get_body(self) -> str:
        """
        Creates html string for the table body including the formatting

        Returns:
            html string
        """

        html_table_body = "<tbody>\n"
        rows = self.model.rowCount()
        columns = self.model.columnCount()

        for row in range(rows):

            txt = "<tr>\n"
            for column in range(columns):
                txt += f'  <td {self._build_style(row, column)}>{self.model.data(self.model.index(row, column))}</td>\n'
            txt += "</tr>\n"

            html_table_body += txt

        html_table_body += "\n</tbody>"
        return html_table_body

    def _get_header(self) -> str:
        """
        Creates html string for the table header row including the formatting

        Returns:
            html string
        """
        txt = "<thead>\n"
        columns = self.model.columnCount()

        txt = "<tr>\n"
        for column in range(columns):
            txt += f'  <th {self._build_style(0, column)}>{self.model.headerData(column, QtCore.Qt.Horizontal)}</th>\n'
        txt += "</tr>\n</thead>"

        return txt

    def get_html(self) -> str:
        """
        Create the final html for the table including the formatting

        Returns:
            html string
        """
        return '<table border="1">\n' + self._get_header() + self._get_body() + '\n</table>'


class Builder:
    """
    Manages creating html for a PyQt Tableview
    """
    def __init__(self, data_model):
        self.style_builder = StyleBuilder()
        self.table_builder = TableBuilder(data_model)
        self.header = None
        self.footer = None

    def add_header(self, header):
        """
        Add the page header
        """
        txt = f'<h1 style="color:#5C6AC4;  text-align: center;">{header}</h1>'
        self.header = txt

    def add_footer(self, footer):
        """
        Add the page footer
        """
        txt = f'<footer style="text-align: right;">{footer}</footer>'
        self.footer = txt

    def get_html(self) -> str:
        """
        Builds the html using all the elements

        Returns:
            ready-to-use html string
        """
        txt = ('<!DOCTYPE html>'
               '<html>'
               '<head>'
               '<style>'
               'table {border-collapse: collapse; width: 100%;}'
               'th {background-color: #ddd; padding: 10px; text-align: left; border: 1px solid #ccc;}'
               'td {padding: 10px; border: 1px solid #ccc;}'
               '</style>'
               '</head>'
               '<body style="padding: 25px;">')

        if self.header:
            txt += self.header

        txt += self.table_builder.get_html()

        if self.footer:
            txt += self.footer

        txt += ("</body>"
                "</html>")

        return txt

    def get_pdf(self, output_filename):
        result_file = open(output_filename, "w+b")

        pisa_status = pisa.CreatePDF(
            self.get_html(),
            dest=result_file)

        result_file.close()

        return pisa_status.err

builder = Builder(TableModel(pd.read_csv("demo_data.csv")))
builder.add_header("Sample Report for demo data")
builder.add_footer("Author: Yuvneesh")

builder.get_pdf("sample.pdf")


