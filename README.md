# LMMR
The package `lmmr` is a collection of Python code I'd like to reuse. Mostly it
consists of simplified interfaces to existing built-in libraries. As an
example, I just want to read and write files, the boiler-plate to open and
close the file can be hidden in my use-cases.

**Note:** Probably you don't want to use this package. It's open-source mostly
for the purpose of having easy access to it. Nevertheless, you're free to use
any of it in your own projects.

## Install
The following instruction are for Linux. You might need to use `pip3` instead of
`pip` depending on your distro.

  1. Clone (or download) the repository.
      ```
      git clone git@github.com:grosheintz/lmmr.git
      ```

  2. Change into the newly cloned repository

     cd lmmr

  3. Use `pip` to install the package locally. If you don't need to edit
  the code:

     pip install --user .

  or as an editably package:

     pip install --user -e .


## License & Copyright
This package is distributed under the MIT license, see LICENSE and was
initially developed at the Seminar of Applied Mathematics at ETH Zurich.

Copyright (c) 2021 ETH Zurich, Luc Grosheintz-Laval
