from .regex import matches_regex_pattern


class TerraformPropertyList:
    def __init__(self, validator):
        self.properties = []
        self.validator = validator

    def property(self, property_name):
        errors = []
        list = TerraformPropertyList(self.validator)
        for property in self.properties:
            if property_name in property.property_value.keys():
                list.properties.append(TerraformProperty(property.resource_type,
                                                         "{0}.{1}".format(property.resource_name,
                                                                          property.property_name),
                                                         property_name,
                                                         property.property_value[property_name]))
            elif self.validator.raise_error_if_property_missing:
                errors.append("[{0}.{1}] should have property: '{2}'".format(property.resource_type,
                                                                             "{0}.{1}".format(property.resource_name,
                                                                                              property.property_name),
                                                                             property_name))

        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

        return list

    def should_equal(self, expected_value):
        errors = []
        for property in self.properties:

            actual_property_value = self.validator.substitute_variable_values_in_string(property.property_value)

            expected_value = self.int2str(expected_value)
            actual_property_value = self.int2str(actual_property_value)
            expected_value = self.bool2str(expected_value)
            actual_property_value = self.bool2str(actual_property_value)

            if actual_property_value != expected_value:
                errors.append("[{0}.{1}.{2}] should be '{3}'. Is: '{4}'".format(property.resource_type,
                                                                                property.resource_name,
                                                                                property.property_name,
                                                                                expected_value,
                                                                                actual_property_value))
        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

    def should_not_equal(self, expected_value):
        errors = []
        for property in self.properties:

            actual_property_value = self.validator.substitute_variable_values_in_string(property.property_value)

            actual_property_value = self.int2str(actual_property_value)
            expected_value = self.int2str(expected_value)
            expected_value = self.bool2str(expected_value)
            actual_property_value = self.bool2str(actual_property_value)

            if actual_property_value == expected_value:
                errors.append("[{0}.{1}.{2}] should not be '{3}'. Is: '{4}'".format(property.resource_type,
                                                                                    property.resource_name,
                                                                                    property.property_name,
                                                                                    expected_value,
                                                                                    actual_property_value))

        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

    def list_should_contain(self, values_list):
        errors = []

        if type(values_list) is not list:
            values_list = [values_list]

        for property in self.properties:

            actual_property_value = self.validator.substitute_variable_values_in_string(property.property_value)
            values_missing = []
            for value in values_list:
                if value not in actual_property_value:
                    values_missing.append(value)

            if len(values_missing) != 0:
                if type(actual_property_value) is list:
                    actual_property_value = [str(x) for x in actual_property_value]  # fix 2.6/7
                errors.append("[{0}.{1}.{2}] '{3}' should contain '{4}'.".format(property.resource_type,
                                                                                 property.resource_name,
                                                                                 property.property_name,
                                                                                 actual_property_value,
                                                                                 values_missing))
        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

    def list_should_not_contain(self, values_list):
        errors = []

        if type(values_list) is not list:
            values_list = [values_list]

        for property in self.properties:

            actual_property_value = self.validator.substitute_variable_values_in_string(property.property_value)
            values_missing = []
            for value in values_list:
                if value in actual_property_value:
                    values_missing.append(value)

            if len(values_missing) != 0:
                if type(actual_property_value) is list:
                    actual_property_value = [str(x) for x in actual_property_value]  # fix 2.6/7
                errors.append("[{0}.{1}.{2}] '{3}' should not contain '{4}'.".format(property.resource_type,
                                                                                     property.resource_name,
                                                                                     property.property_name,
                                                                                     actual_property_value,
                                                                                     values_missing))
        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

    def should_have_properties(self, properties_list):
        errors = []

        if type(properties_list) is not list:
            properties_list = [properties_list]

        for property in self.properties:
            property_names = property.property_value.keys()
            for required_property_name in properties_list:
                if required_property_name not in property_names:
                    errors.append("[{0}.{1}.{2}] should have property: '{3}'".format(property.resource_type,
                                                                                     property.resource_name,
                                                                                     property.property_name,
                                                                                     required_property_name))
        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

    def should_not_have_properties(self, properties_list):
        errors = []

        if type(properties_list) is not list:
            properties_list = [properties_list]

        for property in self.properties:
            property_names = property.property_value.keys()
            for excluded_property_name in properties_list:
                if excluded_property_name in property_names:
                    errors.append(
                        "[{0}.{1}.{2}] should not have property: '{3}'".format(property.resource_type,
                                                                               property.resource_name,
                                                                               property.property_name,
                                                                               excluded_property_name))
        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

    def find_property(self, regex):
        list = TerraformPropertyList(self.validator)
        for property in self.properties:
            for nested_property in property.property_value:
                if matches_regex_pattern(nested_property, regex):
                    list.properties.append(TerraformProperty(property.resource_type,
                                                             "{0}.{1}".format(property.resource_name,
                                                                              property.property_name),
                                                             nested_property,
                                                             property.property_value[nested_property]))
        return list

    def should_match_regex(self, regex):
        errors = []
        for property in self.properties:
            actual_property_value = self.validator.substitute_variable_values_in_string(property.property_value)
            if not matches_regex_pattern(actual_property_value, regex):
                errors.append("[{0}.{1}] should match regex '{2}'".format(property.resource_type,
                                                                          "{0}.{1}".format(property.resource_name,
                                                                                           property.property_name),
                                                                          regex))

        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

    def bool2str(self, bool):
        if str(bool).lower() in ["true"]:
            return "True"
        if str(bool).lower() in ["false"]:
            return "False"
        return bool

    def int2str(self, property_value):
        if type(property_value) is int:
            property_value = str(property_value)
        return property_value


class TerraformProperty:
    def __init__(self, resource_type, resource_name, property_name, property_value):
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.property_name = property_name
        self.property_value = property_value