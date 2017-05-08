===============================
python-iotronicclient
===============================

Iotronic Client

Client for the IoTronic service.

.. contents:: Contents:
   :local:

Installing
----------------------
Clone the repo and install the client::

    git clone https://github.com/openstack/python-iotronicclient.git
    cd python-iotronicclient
    pip install -r requirements.txt
    python setup.py install

Usage
----------------------
help::

   iotronic --help
   
::

   Command-line interface to the Iotronic API.

   Positional arguments:
     <subcommand>
       board-create        Register a new board with the Iotronic service.
       board-delete        Unregister board(s) from the Iotronic service.
       board-list          List the boards which are registered with the Iotronic
                           service.
       board-show          Show detailed information about a board.
       board-update        Update information about a registered board.
       plugin-create       Register a new plugin with the Iotronic service.
       plugin-delete       Unregister plugin(s) from the Iotronic service.
       plugin-list         List the plugins which are registered with the
                           Iotronic service.
       plugin-show         Show detailed information about a plugin.
       plugin-update       Update information about a registered plugin.
       plugin-action       Execute an action of the plugin.
       plugin-inject       Inject a plugin into a board.
       plugin-remove       Remove a plugin from a board.
       plugins-on-board    Show information about a the plugins injected on a
                           board.
       bash-completion     Prints all of the commands and options for bash-
                           completion.
       help                Display help about this program or one of its
                           subcommands.


* Free software: Apache license
* Source: http://git.openstack.org/cgit/openstack/python-iotronicclient
* Bugs: http://bugs.launchpad.net/python-iotronicclient
