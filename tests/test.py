#!/usr/bin/env python3
''' Acceptance test suite for mlx.xunit2rst

The tests in this file are pure black box tests. They just check whether the
outputs of the tool match the reference output files exactly.
'''

from subprocess import check_call
import filecmp
from pathlib import Path

import nose
from nose.tools import with_setup

TOP_DIR = Path(__file__).parents[1]
TEST_OUT_DIR = Path(__file__).parent / 'test_out'
TEST_IN_DIR = Path(__file__).parent / 'test_in'

def setup():
    ''' Setup function

    This function creates the output directory for mlx.xunit2rst to put the
    output files
    '''
    TEST_OUT_DIR.mkdir(exist_ok=True)


def xunit2rst_check(input_xml, output_rst, prefix, trim_suffix=False):
    ''' Helper function for testing whether mlx.xunit2rst produces the expected output '''

    command = 'mlx.xunit2rst -i {} -o {} -p {}'.format(input_xml, output_rst, prefix)
    if trim_suffix:
        command += ' --trim-suffix'

    return_code = check_call(command, shell=True)
    print(command)
    assert return_code == 0


@with_setup(setup)
def xunit_test():
    '''Tests based on reports generated by `robot --xunit` '''
    file_name = 'itest_report'
    rst_file_name = '{}.rst'.format(file_name)
    xml_file_name = '{}.xml'.format(file_name)
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst, 'ITEST_-', True)

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


if __name__ == '__main__':
    nose.main()
