# avro2py 
Avro codegen for Python 3.6+. Supports Avro v.1.10.0.

## Installation and usage
```bash
$ pip install avro2py
$ avro2py my_schema.avsc  # will generate code in current directory
```

## TODOs and warnings
This library does not support the following Avro features:
- Aliases (http://avro.apache.org/docs/1.10.0/spec.html#Aliases)
- Default values (http://avro.apache.org/docs/1.10.0/spec.html#schema_record)

and additionally comes with the following caveats:
- No checks are made for circular dependencies in rendered code
- Name shadowing from cross-module imports is not prevented