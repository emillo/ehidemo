===============================
ehidemo
===============================


Demo of a notification manager, execution  for this assignment_


* Free software: MIT license
* Documentation: TODO


Implementation
**************

* it loads in memory the list of customers and their corresponding
  notification_labels
  
* it receives notifications in GET through the HTTPHandler_ class, analyzes
  the query string and validates the input trhough the InputValidator_
  class. It verifies that only one payload is provided in GET parameters,
  and that both label and payload parameters are present and not empty
  otherwise it gives an HTTP 406 error.
  
* it searches in the list of customers if the notification_label is present
  and retrieves its corresponding customer_id

* it stores in the database (accessed through the Database_ class and the
  DAO_ class) the notification with the relative customer_id, and updates
  the daily count of notifications for that customer.

* if more than one label is provided in input, it stores a stray
  notification  (with customer_id empty)

* it logs events and errors in the file "ehidemo.log"
  
Installation
************

install sqlite3:

.. code:: bash

		  sudo apt install sqlite3


go in the cloned directory and create the database:

.. code:: bash
		  
		  sqlite3 ehidemo.db < schema.sql

go in the cloned directory and create a python3 virtualenv:

.. code:: bash

		  virtualenv -p python3 .
		  source bin/activate

install pytest:

.. code:: bash

		  pip install pytest

run the tests:

.. code:: bash

		  pytest tests/

start the server:

.. code:: bash

		  python3 -m ehidemo.ehidemo
		  

Examples:
*********

You can use curl to send notifications to the server at "http://localhost:30123"
or "http://127.0.0.1:30123".

* example of ok transaction:

.. code:: bash

		  curl "http://127.0.0.1:30123/?label=Kinshasa&payload=123456"

response:

.. code::

   HTTP/1.0 200 OK

.. code:: json


   {
     "status": "ok",
     "notification": "notification success for customer 7"
   }


* example of not ok transaction:

.. code:: bash

   curl "http://localhost:30123/?label=&payload=1234567890abcd"

response:
  
.. code::

   HTTP/1.0 406 Not Acceptable

.. code::

   Input error: field 'label' missing

   
Credits
*******

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _assignment: assignment.md
.. _HTTPHandler: https://github.com/emillo/ehidemo/blob/2d788712d1372247d9041e5ef31326faecf594cf/ehidemo/ehidemo.py#L74
.. _InputValidator: https://github.com/emillo/ehidemo/blob/47e0a048ef8fc003185324ee10f325009bbcf504/ehidemo/ehidemo.py#L57
.. _Database: https://github.com/emillo/ehidemo/blob/47e0a048ef8fc003185324ee10f325009bbcf504/ehidemo/database.py#L6
.. _DAO: https://github.com/emillo/ehidemo/blob/47e0a048ef8fc003185324ee10f325009bbcf504/ehidemo/ehidemo.py#L21

































