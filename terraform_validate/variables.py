from .regex import matches_regex_pattern


class TerraformVariableParser:
    def __init__(self, string):
        self.string = string
        self.functions = []
        self.variable = ""
        self.state = 0
        self.index = 0

    def parse(self):
        while self.index < len(self.string):
            if self.state == 0:
                if self.string[self.index:self.index + 3] == "var":
                    self.index += 3
                    self.state = 1
                else:
                    self.state = 3
                    temp_function = ""
            if self.state == 1:
                temp_var = ""
                while True:
                    self.index += 1
                    if self.index == len(self.string) or self.string[self.index] == ")":
                        self.variable = temp_var
                        self.state = 2
                        break;
                    else:
                        temp_var += self.string[self.index]
            if self.state == 2:
                self.index += 1
            if self.state == 3:
                if self.string[self.index] == "(":
                    self.state = 0
                    self.functions.append(temp_function)
                else:
                    temp_function += self.string[self.index]
                self.index += 1


class TerraformVariableList:
    def __init__(self, variables):
        self.variables = variables

    def variable(self, var_name):
        if var_name not in self.variables.keys():
            raise AssertionError("There is no Terraform variable '{0}'".format(var_name))
        return TerraformVariable(var_name, self.variables[var_name])

    def has_no_variable(self, var_name):
        if var_name in self.variables.keys():
            raise AssertionError("There is Terraform variable '{0}'".format(var_name))
        return self


class TerraformVariable:
    def __init__(self, var_name, variable):
        self.var_name = var_name
        self.variable = variable

    def has_default(self):
        self.__find_value_for_type__('default')

    def no_default_value(self):
        self.__check_no_value_for_type('default')

    def default_value_equals(self, expected_value):
        default = self.__find_value_for_type__('default')
        if default != expected_value:
            raise AssertionError("Variable '{0}' should have a default value of {1}. Is: {2}".format(self.var_name,
                                                                                                     expected_value,
                                                                                                     default))

    def default_value_matches_regex(self, regex):
        default = self.__find_value_for_type__('default')
        if not matches_regex_pattern(default, regex):
            raise AssertionError(
                "Variable '{0}' should have a default value that matches regex '{1}'. Is: {2}".format(self.var_name,
                                                                                                      regex,
                                                                                                      default))

    def has_value(self):
        self.__find_value_for_type__('default')

    def no_value(self):
        self.__check_no_value_for_type('value')

    def value_equals(self, expected_value):
        value = self.__find_value_for_type__('value')
        if value != expected_value:
            raise AssertionError("Variable '{0}' should have a value of {1}. Is: {2}".format(self.var_name,
                                                                                             expected_value,
                                                                                             value))

    def value_matches_regex(self, regex):
        value = self.__find_value_for_type__('value')
        if not matches_regex_pattern(value, regex):
            "Variable '{0}' should have a default value that matches regex '{1}'. Is: {2}".format(self.var_name,
                                                                                                  regex,
                                                                                                  value)

    def __check_no_value_for_type(self, value_type):
        if value_type in self.variable.keys():
            raise AssertionError("Variable '{0}' has a '{1}' value".format(self.var_name, value_type))

    def __find_value_for_type__(self, value_type):
        if value_type not in self.variable.keys():
            raise AssertionError("Variable '{0}' has no '{1}' value".format(self.var_name, value_type))

        return self.variable[value_type]
