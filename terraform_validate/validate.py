import hcl
import os
import re
from .types import TerraformTypeList, TerraformSection
from .variables import TerraformVariableList, TerraformVariableParser


# def deprecated(func):
#     '''This is a decorator which can be used to mark functions
#     as deprecated. It will result in a warning being emitted
#     when the function is used.'''
#     def new_func(*args, **kwargs):
#         print("The method '{0}' is deprecated as of v2.0. Please refer to the readme for the recommended usage of this library.".format(func.__name__))
#         print("'{0}' will be removed in a future release.".format(func.__name__))
#         return func(*args, **kwargs)
#     new_func.__name__ = func.__name__
#     new_func.__doc__ = func.__doc__
#     new_func.__dict__.update(func.__dict__)
#     return new_func

class TerraformSyntaxException(Exception):
    pass


class TerraformVariableException(Exception):
    pass


class TerraformUnimplementedInterpolationException(Exception):
    pass


class Validator:
    def __init__(self, path=None):
        self.variable_expand = False
        self.raise_error_if_property_missing = False
        if type(path) is not dict:
            if path is not None:
                self.terraform_config = self.parse_terraform_directory(path)
        else:
            self.terraform_config = path

    def __get_sections__(self, section_name):
        return self.terraform_config[section_name] if section_name in self.terraform_config.keys() else {}

    # TODO add in resource by name
    def resources(self):
        return TerraformSection(self, 'resource', self.__get_sections__('resource'))
        # return TerraformTypeList(self, type_name, self.__get_sections__('resource'))

    def data(self, type_name):
        return TerraformTypeList(self, type_name, self.__get_sections__('data'))

    def variables(self):
        return TerraformVariableList(self.__get_sections__('variable'))

    def enable_variable_expansion(self):
        self.variable_expand = True

    def disable_variable_expansion(self):
        self.variable_expand = False

    def error_if_property_missing(self):
        self.raise_error_if_property_missing = True

    def parse_terraform_directory(self, path):
        terraform_string = ""
        for directory, subdirectories, files in os.walk(path):
            for file in files:
                if file.endswith(".tf"):
                    with open(os.path.join(directory, file)) as fp:
                        new_terraform = fp.read()
                        try:
                            hcl.loads(new_terraform)
                        except ValueError as e:
                            raise TerraformSyntaxException(
                                "Invalid terraform configuration in {0}\n{1}".format(os.path.join(directory, file), e))
                        terraform_string += new_terraform
        terraform = hcl.loads(terraform_string)
        return terraform

    def get_terraform_resources(self, name, resources):
        if name not in resources.keys():
            return []
        return self.convert_to_list(resources[name])

    def substitute_variable_values_in_string(self, s):
        if self.variable_expand:
            if not isinstance(s, dict):
                for variable in self.list_terraform_variables_in_string(s):
                    a = TerraformVariableParser(variable)
                    a.parse()
                    variable_default_value = self.get_terraform_variable_value(a.variable)
                    if variable_default_value != None:
                        for function in a.functions:
                            if function == "lower":
                                variable_default_value = variable_default_value.lower()
                            elif function == "upper":
                                variable_default_value = variable_default_value.upper()
                            else:
                                raise TerraformUnimplementedInterpolationException(
                                    "The interpolation function '{0}' has not been implemented in Terraform Validator yet. Suggest you run disable_variable_expansion().".format(
                                        function))
                        s = s.replace("${" + variable + "}", variable_default_value)
        return s

    def list_terraform_variables_in_string(self, s):
        return re.findall('\${(.*?)}', str(s))

    def convert_to_list(self, nested_resources):
        if not type(nested_resources) == list:
            nested_resources = [nested_resources]
        return nested_resources

    def get_terraform_variable_value(self,variable):
        if ('variable' not in self.terraform_config.keys()) or (variable not in self.terraform_config['variable'].keys()):
            raise TerraformVariableException("There is no Terraform variable '{0}'".format(variable))
        if 'default' not in self.terraform_config['variable'][variable].keys():
            return None
        return self.terraform_config['variable'][variable]['default']
