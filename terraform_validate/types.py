from .regex import matches_regex_pattern
from .properties import TerraformPropertyList, TerraformProperty


class TerraformSection:
    def __init__(self, validator, section_name, section):
        self.validator = validator
        self.section_name = section_name
        self.section = section

    def __add_section_types__(self, type_list, sections, single_type):
        for resource in sections[single_type]:
            type_list.append(TerraformType(single_type, resource, sections[single_type][resource]))

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

    def types_by_list(self, type_names):
        type_list = []
        for type_name in type_names:
            self.__add_section_types__(type_list, self.section, type_name)
        return TerraformTypeList(self.validator, type_list, type_name)

    def types_by_name(self, type_name):
        self.has_type(type_name)

        type_list = []
        self.__add_section_types__(type_list, self.section, type_name)
        return TerraformTypeList(self.validator, type_list, type_name)

    def types_like(self, type_regex):
        self.has_type_like(type_regex)

        type_list = []
        for single_type in self.section.keys():
            if matches_regex_pattern(single_type, type_regex):
                self.__add_section_types__(type_list, self.section, single_type)

        return TerraformTypeList(self.validator, type_list, type_regex)


class TerraformType:
    def __init__(self, type, id, config):
        self.type = type
        self.id = id
        self.config = config


class TerraformTypeList:
    # TODO add in get resource by
    # Tag
    # Name
    # Id
    def __init__(self, validator, type_list, type_name_or_regex):
        self.validator = validator
        self.type_list = type_list
        self.type_name_or_regex = type_name_or_regex

    def property(self, property_name):
        errors = []
        list = TerraformPropertyList(self.validator)
        if len(self.type_list) > 0:
            for type_value in self.type_list:
                if property_name in type_value.config.keys():
                    list.properties.append(
                        TerraformProperty(type_value.type, type_value.id, property_name,
                                          type_value.config[property_name]))
                elif self.validator.raise_error_if_property_missing:
                    errors.append(
                        "[{0}.{1}] should have property: '{2}'".format(type_value.type, type_value.id, property_name))

        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

        return list

    def find_property(self, regex):
        list = TerraformPropertyList(self.validator)
        if len(self.type_list) > 0:
            for type_value in self.type_list:
                for property in type_value.config:
                    if matches_regex_pattern(property, regex):
                        list.properties.append(TerraformProperty(type_value.type,
                                                                 type_value.id,
                                                                 property,
                                                                 type_value.config[property]))
        return list

    def should_have_properties(self, properties_list):
        errors = []

        if type(properties_list) is not list:
            properties_list = [properties_list]

        if len(self.type_list) > 0:
            for type_value in self.type_list:
                property_names = type_value.config.keys()
                for required_property_name in properties_list:
                    if required_property_name not in property_names:
                        errors.append(
                            "[{0}.{1}] should have property: '{2}'".format(type_value.type,
                                                                           type_value.id,
                                                                           required_property_name))
        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

    def should_not_have_properties(self, properties_list):
        errors = []

        if type(properties_list) is not list:
            properties_list = [properties_list]

        if len(self.type_list) > 0:
            for type_value in self.type_list:
                property_names = type_value.config.keys()
                for excluded_property_name in properties_list:
                    if excluded_property_name in property_names:
                        errors.append(
                            "[{0}.{1}] should not have property: '{2}'".format(type_value.type,
                                                                               type_value.id,
                                                                               excluded_property_name))
        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))

    def name_should_match_regex(self, regex):
        errors = []
        for resource in self.type_list:
            if not matches_regex_pattern(resource.id, regex):
                errors.append("[{0}.{1}] name should match regex '{2}'".format(resource.type, resource.id, regex))

        if len(errors) > 0:
            raise AssertionError("\n".join(sorted(errors)))
