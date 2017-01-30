# Terraform Validate

A python package for testing Terraform's infrastructure as code though user-defined standards.

Uses `pyhcl` to parse Terraform configuration files, allowing users to write custom scripts to test Terraform. 
By testing Terraform scripts time is saved in validating scripts before running Terraform apply.

## API

The declarative API allows testing scripts to be developed quickly. Any checks throw an `AssertionError` when
the values that they are looking for are not found. In some cases these assertions can be suppressed.
The API is made up of different sections which represent different areas of the Terraform scripts:

### Validator

The validator is an entrypoint in to the Terraform scripts, parsing them and allowing basic sections (resources, data
variables) to be retrieved and then tested.

The validator is set up using the following:
```
from terrform_validate import Validator

validator = Validator(os.path.join(self.path, "path/to/terraform/scripts"))
```

The Validator has three main functions which retrieve different sections of the Terraform scripts:
- `resources()` - returns anything that starts with `resource`
- `data()` - returns any data-source starting with `data`
- `variables()` - returns the variable sections starting with `variable`

### Resources (and Data)

As the most common part of the infrastructure code most of the testing will be related to resources or data and their 
properties. Getting these is a case of calling `resources()` or `data()` on the `Validator` as such.

```
from terrform_validate import Validator

validator = Validator(os.path.join(self.path, "path/to/terraform/scripts"))
# get resources
validator.resources()

# get data sources
validator.data()
```

This returns a `TerraformSection`, a class which allows you to find and check types by type name (aws_instance), and id.
None of these throw an `AssertionError`, if values aren't found. The `TerraformSection` returns a `TerraformTypeList`
that can be used to validate the types returned. These are as follows:
```
# Get aws_instance types by name
validator.resources().types_by_name('aws_instance')

# Get types related to security
validator.resources().types_like('.*security.*')

# Get types with a specific id
validator.resources().types_by_id('bastion_host')

# Get types with an id that contains host
validator.resources().types_id_like('.*host.*')

# Get aws_subnet and aws_security_group types
valiator.resources().types_by_names(['aws_instance', 'aws_security_group'])

# Get all types
validator.resources().all_types()
```

You can assert that a section has certain types:
```
# make sure that there is data from an archive file
validator.data().has_type('archive_file')

# make sure that there are archive types
validator.data().has_type_like('archive.*')

# make sure that there are types of each name
validator.data().has_types(['archive_file', 'external'])

# Make sure there are types with a specific id
validator.data().has_type_by_id('local_data_source')
```

### Types

Types represent anything that is under the `resources` or `data` sections. When querying a section for a list of types 
an instance of `TerraformTypeList` is returned. This allows can be used to filter the types and validate them and
their properties.

#### Terraform Type List

### Properties

### Variables

