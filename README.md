# avro2py 
Avro codegen for Python 3.

## Development
All library code must live within the `avro2py/` directory.


## Usage

To use this library (or any Teika python library), you will need to import it from our cloudrepo instance of PyPi
Put the following code in your Dockerfile to allow installs of Teikametrics internal libraries:

`ADD requirements.txt /tmp/requirements.txt`
`RUN pip install -r /tmp/requirements.txt --extra-index-url "https://$CLOUDREPO_USERNAME:$CLOUDREPO_PASSWORD@teikametrics.mycloudrepo.io/repositories/teika-pypi"`

The necessary values for CLOUDREPO_USERNAME and CLOUDREPO_PASSWORD are stored in 1Password, under `CloudRepo CircleCI User`, and should be added to the CircleCI build environment.
NOTE: Pin the library version exactly in your requirements.txt file. Otherwise, the library you are expecting may not be the one you get.

## Deployment

* This library is automatically re-built after a successful PR to master.
* When opening a PR on a new branch, you must increment the `version=X.X.X` argument in the `setup.py` file. Otherwise,
CI will fail.
