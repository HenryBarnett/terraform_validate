import re
import os
import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import terraform_validate as t

class TestValidatorDataFunctional(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    def error_list_format(self,error_list):
        if type(error_list) is not list:
            error_list = [error_list]
        regex = "\n".join(map(re.escape,error_list))
        return "^{0}$".format(regex)

    def test_data(self):
        validator = t.Validator(os.path.join(self.path,"fixtures/data"))
        validator.data('template_file').property('template').should_equal('${file("${path.module}/init.tpl")}')
        expected_error = self.error_list_format([
            "[aws_instance.bar.value] should be '2'. Is: '1'",
            "[aws_instance.foo.value] should be '2'. Is: '1'"
        ])
        with self.assertRaisesRegexp(AssertionError, expected_error):
            validator.resources('aws_instance').property('value').should_equal(2)