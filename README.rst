``longtroll``
===========
*Detect long-running processes and notify you when they're done.*

Using ``longtroll``
-----------------

``longtroll`` pretty much does what it says on the box. In order to start
detecting long-running processes, run ``longtroll.py bind`` in your shell. From
then on, when a long-running process in that shell finishes, your notification
command will be called.

Before you start using ``longtroll``, you need to create a configuration file.
A sample configuration file can be found in the repository as
``longtrollrc-sample``. Copy this file to ``~/.longtrollrc``, or create your own.
The configuration file takes two options: ``seconds`` and ``notify``, as
follows::
  
    seconds 10
    notify echo <cmd> (pid <pid>) completed | wall

``seconds`` is the number of seconds that a process has to live before it is
considered "long-running". ``notify`` is a command that will be run when your
process completes. The tokens ``<cmd>`` and ``<pid>`` will automatically be replaced
by the command and the PID of the process that completed.

Roadmap
-------

* Add a ``longtroll.py unbind`` command

* Allow configuration of the poll time

* Some kind of notification method for when a long-running process is detected
