# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import nose
from nose.tools import assert_equal
from datetime import datetime
from xlwings import Workbook, Range

# Optional imports
try:
    import numpy as np
    from numpy.testing import assert_array_equal
except ImportError:
    np = None
try:
    import pandas as pd
    from pandas import DataFrame
    from pandas.util.testing import assert_frame_equal
except ImportError:
    pd = None

# Connect to test file and make Sheet1 the active sheet
xl_file1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test1.xlsx')
wb = Workbook(xl_file1)
wb.activate('Sheet1')

# Test data
data = [[1, 2.222, 3.333],
        ['Test1', None, 'éöà'],
        [datetime(1962, 11, 3), datetime(2020, 12, 31, 12, 12, 20), 9.999]]

test_date_1 = datetime(1962, 11, 3)
test_date_2 = datetime(2020, 12, 31, 12, 12, 20)

list_row_1d = [1.1, None, 3.3]
list_row_2d = [[1.1, None, 3.3]]
list_col = [[1.1], [None], [3.3]]

if np is not None:
    array_1d = np.array([1.1, 2.2, np.nan, -4.4])
    array_2d = np.array([[1.1, 2.2, 3.3], [-4.4, 5.5, np.nan]])


# Test skips and fixtures
def _skip_if_no_numpy():
    if np is None:
        raise nose.SkipTest('numpy missing')


def _skip_if_no_pandas():
    if pd is None:
        raise nose.SkipTest('pandas missing')


# def teardown_module():
#     wb.close()


def test_cell():
    params = [('A1', 22),
              ((1,1), 22),
              ('A1', 22.2222),
              ((1,1), 22.2222),
              ('A1', 'Test String'),
              ((1,1), 'Test String'),
              ('A1', 'éöà'),
              ((1,1), 'éöà'),
              ('A2', test_date_1),
              ((2,1), test_date_1),
              ('A3', test_date_2),
              ((3,1), test_date_2)]
    for param in params:
        yield check_cell, param[0], param[1]


def check_cell(address, value):
    # Active Sheet
    Range(address).value = value
    cell = Range(address).value
    assert_equal(cell, value)

    # SheetName
    Range('Sheet2', address).value = value
    cell = Range('Sheet2', address).value
    assert_equal(cell, value)

    # SheetIndex
    Range(3, address).value = value
    cell = Range(3, address).value
    assert_equal(cell, value)


def test_range_address():
    """ Style: Range('A1:C3') """
    address = 'C1:E3'

    # Active Sheet
    Range(address[:2]).value = data  # assign to starting cell only
    cells = Range(address).value
    assert_equal(cells, data)

    # Sheetname
    Range('Sheet2', address).value = data
    cells = Range('Sheet2', address).value
    assert_equal(cells, data)

    # Sheetindex
    Range(3, address).value = data
    cells = Range(3, address).value
    assert_equal(cells, data)


def test_range_index():
    """ Style: Range((1,1), (3,3)) """
    index1 = (1,3)
    index2 = (3,5)

    # Active Sheet
    Range(index1, index2).value = data
    cells = Range(index1, index2).value
    assert_equal(cells, data)

    # Sheetname
    Range('Sheet2', index1, index2).value = data
    cells = Range('Sheet2', index1, index2).value
    assert_equal(cells, data)

    # Sheetindex
    Range(3, index1, index2).value = data
    cells = Range(3, index1, index2).value
    assert_equal(cells, data)


def test_named_range():
    value = 22.222
    # Active Sheet
    Range('cell_sheet1').value = value
    cells = Range('cell_sheet1').value
    assert_equal(cells, value)

    Range('range_sheet1').value = data
    cells = Range('range_sheet1').value
    assert_equal(cells, data)

    # Sheetname
    Range('Sheet2', 'cell_sheet2').value = value
    cells = Range('Sheet2', 'cell_sheet2').value
    assert_equal(cells, value)

    Range('Sheet2', 'range_sheet2').value = data
    cells = Range('Sheet2', 'range_sheet2').value
    assert_equal(cells, data)

    # Sheetindex
    Range(3, 'cell_sheet3').value = value
    cells = Range(3, 'cell_sheet3').value
    assert_equal(cells, value)

    Range(3, 'range_sheet3').value = data
    cells = Range(3, 'range_sheet3').value
    assert_equal(cells, data)


def test_array():
    _skip_if_no_numpy()

    # 1d array
    Range('Sheet6', 'A1').value = array_1d
    cells = Range('Sheet6', 'A1:D1', asarray=True).value
    assert_array_equal(cells, array_1d)

    # 2d array
    Range('Sheet6', 'A4').value = array_2d
    cells = Range('Sheet6', 'A4', asarray=True).table.value
    assert_array_equal(cells, array_2d)

    # 1d array (atleast_2d)
    Range('Sheet6', 'A10').value = array_1d
    cells = Range('Sheet6', 'A10:D10', asarray=True, atleast_2d=True).value
    assert_array_equal(cells, np.atleast_2d(array_1d))

    # 2d array (atleast_2d)
    Range('Sheet6', 'A12').value = array_2d
    cells = Range('Sheet6', 'A12', asarray=True, atleast_2d=True).table.value
    assert_array_equal(cells, array_2d)


def test_vertical():
    Range('Sheet4', 'A10').value = data
    cells = Range('Sheet4', 'A10').vertical.value
    assert_equal(cells, [row[0] for row in data])


def test_horizontal():
    Range('Sheet4', 'A20').value = data
    cells = Range('Sheet4', 'A20').horizontal.value
    assert_equal(cells, data[0])


def test_table():
    Range('Sheet4', 'A1').value = data
    cells = Range('Sheet4', 'A1').table.value
    assert_equal(cells, data)


def test_list():

    # 1d List Row
    Range('Sheet4', 'A27').value = list_row_1d
    cells = Range('Sheet4', 'A27:C27').value
    assert_equal(list_row_1d, cells)

    # 2d List Row
    Range('Sheet4', 'A29').value = list_row_2d
    cells = Range('Sheet4', 'A29:C29', atleast_2d=True).value
    assert_equal(list_row_2d, cells)

    # 1d List Col
    Range('Sheet4', 'A31').value = list_col
    cells = Range('Sheet4', 'A31:A33').value
    assert_equal([i[0] for i in list_col], cells)
    # 2d List Col
    cells = Range('Sheet4', 'A31:A33', atleast_2d=True).value
    assert_equal(list_col, cells)


def test_clear_content():
    Range('Sheet4', 'G1').value = 22
    Range('Sheet4', 'G1').clear_contents()
    cell = Range('Sheet4', 'G1').value
    assert_equal(cell, None)


def test_clear():
    Range('Sheet4', 'G1').value = 22
    Range('Sheet4', 'G1').clear()
    cell = Range('Sheet4', 'G1').value
    assert_equal(cell, None)


def test_dataframe():
    _skip_if_no_pandas()

    df_expected = DataFrame({'a': [1, 2, 3.3, np.nan], 'b': ['test1', 'test2', 'test3', None]})
    Range('Sheet5', 'A1').value = df_expected
    cells = Range('Sheet5', 'B1:C5').value
    df_result = DataFrame(cells[1:], columns=cells[0])
    assert_frame_equal(df_expected, df_result)


def test_none():
    """ Covers Issue #16"""
    # None
    Range('Sheet1', 'A7').value = None
    assert_equal(None, Range('Sheet1', 'A7').value)
    # List
    Range('Sheet1', 'A7').value = [None, None]
    assert_equal(None, Range('Sheet1', 'A7').horizontal.value)


def test_scalar_nan():
    """Covers Issue #15"""
    _skip_if_no_numpy()

    Range('Sheet1', 'A20').value = np.nan
    assert_equal(None, Range('Sheet1', 'A20').value)

if __name__ == '__main__':
    nose.main()