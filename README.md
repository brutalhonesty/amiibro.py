Amiibro Python Script
================

Queries Amiibro Service and prints out the data nicely.


Requirements
------------------

* Python 2.7+
* [requests](https://pypi.python.org/pypi/requests)
* [colorama](https://pypi.python.org/pypi/colorama)

Usage
---------

```bash
# Check Python version
$ python --version
2.7.6

# Check for Amiibo and give US Zipcode
$ ./main.py -n samus -z 30096

# Give radius as well (in miles)
$ ./main.py -n samus -z 30096 -r 100

# Print out the Amiibo names and their SKUs
$ ./main.py -nn
```

License
-----------

* [MIT](http://brutalhonesty.mit-license.org/)
* [TL;DR](https://tldrlegal.com/license/mit-license)