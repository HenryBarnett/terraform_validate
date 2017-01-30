from .regex import matches_regex_pattern
from .properties import TerraformPropertyList, TerraformProperty


class TerraformSection:
    def __init__(self, validator, section_name, section):
        self.validator = validator
        self.section_name = section_name
        self.section = section

    # TODO add in get resource by
    # Tag
    # property value?

    def __add_section_types__(self, type_list, type_name):
        for type_id in self.section[type_name]:
            type_list.append(TerraformType(type_name, type_id, self.section[type_name][type_id]))

    def has_types(self, type_names):
        for type_name in type_names:
            self.has_type(type_name)
        return self

    def has_type(self, type_name):
        if type_name not in self.section.keys():
            raise AssertionError("Unable to find type {0} in Terraform scripts.".format(type_name))
        return self

    def has_type_like(self, regex):
        found = False
        for single_type in self.section.keys():
            if matches_regex_pattern(single_type, regex):
                found = True

        if not found:
            raise AssertionError("Unable to find type like {0} in Terraform scripts.".format(regex))
        return self

    def has_type_by_id(self, lookup_id):
        pass

    def types_by_names(self, type_names):
        type_list = []
        for type_name in type_names:
            self.__add_section_types__(type_list, type_name)
        return TerraformTypeList(self.validator, type_list, type_name)

    def types_by_name(self, type_name):
        self.has_type(type_name)

        type_list = []
        self.__add_section_types__(type_list, type_name)
        return TerraformTypeList(self.validator, type_list, type_name)

    def types_by_id(self, lookup_id):
        type_list = []
        for type_name, type_value in self.section.items():
            if lookup_id in type_value.keys():
                type_list.append(TerraformType(type_name, lookup_id, type_value[lookup_id]))

        return TerraformTypeList(self.validator, type_list, lookup_id)

    def type_id_like(self, id_regex):
        type_list = []
        for type_name, type_value in self.section.items():
            for type_id in type_value.keys():
                if matches_regex_pattern(type_id, id_regex):
                    type_list.append(TerraformType(type_name, type_id, type_value[type_id]))

        return TerraformTypeList(self.validator, type_list, id_regex)

    def types_like(self, type_regex):
        self.has_type_like(type_regex)

        type_list = []
        for single_type in self.section.keys():
            if matches_regex_pattern(single_type, type_regex):
                self.__add_section_types__(type_list, single_type)

        return TerraformTypeList(self.validator, type_list, type_regex)

    def all_types(self):
        type_list = []
        for type_name, types in self.section.items():
            for type_id, type_value in types.items():
                type_list.append(TerraformType(type_name, type_id, type_value))

        return TerraformTypeList(self.validator, type_list, 'all')


class TerraformType:
    def __init__(self, type_name, id, config):
        self.type_name = type_name
        self.id = id
        self.config = config


class TerraformTypeList:
    def __init__(self, validator, type_list, type_name_or_regex):
        self.validator = validator
        self.type_list = type_list
        self.type_name_or_regex = type_name_or_regex
        self.raise_error_if_property_missing = False

    def __property_by_name__(self, property_name):
        errors = []
        property_list = TerraformPropertyList(self.validator)
        if not self.type_list:
            errors.append(
                "No properties on type, cannot find {0}.".format(property_name))
        else:
            for type_value in self.type_list:
                if property_name in type_value.config.keys():
                    property_list.properties.append(
                        TerraformProperty(type_value.type_name,
                                          type_value.id,
                                          property_name,
                                          type_value.config[property_name]))
                else:
                    errors.append(
                        "[{0}.{1}] should have property: '{2}'".format(type_value.type_name, type_value.id, property_name))

        return property_list, errors

    def error_if_property_missing(self, should_error):
        self.raise_error_if_property_missing = should_error
        return self

    def property(self, property_name):
        (property_list, errors) = self.__property_by_name__(property_name)

        if self.raise_error_if_property_missing and len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

        return property_list

    def have_property(self, property_name):
        (_, errors) = self.__property_by_name__(property_name)
        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))
        return self

    def properties_like(self, regex):
        property_list = TerraformPropertyList(self.validator)
        for type_value in self.type_list:
            for property_value in type_value.config:
                if matches_regex_pattern(property_value, regex):
                    property_list.properties.append(TerraformProperty(type_value.type_name,
                                                                      type_value.id,
                                                                      property_value,
                                                                      type_value.config[property_value]))
        return property_list

    def have_properties(self, properties_list):
        errors = []

        if type(properties_list) is not list:
            properties_list = [properties_list]

        for property_name in properties_list:
            _, new_errors = self.__property_by_name__(property_name)
            errors.extend(new_errors)

        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))
        return self

    def do_not_have_properties(self, properties_list):
        errors = []

        if type(properties_list) is not list:
            properties_list = [properties_list]

        for type_value in self.type_list:
            property_names = type_value.config.keys()
            for excluded_property_name in properties_list:
                if excluded_property_name in property_names:
                    errors.append(
                        "[{0}.{1}] should not have property: '{2}'".format(type_value.type_name,
                                                                           type_value.id,
                                                                           excluded_property_name))
        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

    def filter_id(self, filter_id):
        new_type_list = []
        for type_value in self.type_list:
            if type_value.id == filter_id:
                new_type_list.append(TerraformType(type_value.type_name,
                                                   type_value.id,
                                                   type_value))

        return TerraformTypeList(self.validator, new_type_list, "{0}.{1}".format(self.type_name_or_regex, filter_id))

    def have_id_like(self, regex):
        errors = []
        for type_value in self.type_list:
            if not matches_regex_pattern(type_value.id, regex):
                errors.append(
                    "[{0}.{1}] name should match regex '{2}'".format(type_value.type_name, type_value.id, regex))

        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

        return self

    def is_size(self, size):
        cur_size = len(self.type_list)
        if cur_size != size:
            raise AssertionError("Type list '{0}' should have size {1} but has size {2}.".format(self.type_name_or_regex,
                                                                                               size,
                                                                                               cur_size))
        return self
