# DEFT-CLI
If you are reading this, you are looking at the code repository of the DEFT project,
which name stands for "Database Engine For Tasks". Documentaiton is maintained on
the pages accessible from the following URL (CERN auth/auth required):

https://twiki.cern.ch/twiki/bin/viewauth/AtlasComputing/WorkFlow

DEFT is an assembly of a few service modules and key Python classes, which can be driven
from a Command Line Interface (CLI) or any other application. The CLI app is described
below:


Synopsis (to be changed as needed):

% deft-cli.py -h
usage: deft.py [-h] [-d DEBUG] [-t TEMPLATE] [-i IN_META] [-o OUT_META]
               [-p PURGE] [-s] [-r RETRIEVE] [-f FETCH] [-T UPDATE_TASK]
               [-D UPDATE_DATASET] [-x]

optional arguments:
  -h, --help            show this help message and exit
  -d DEBUG, --debug DEBUG
                        DEBUG level
  -t TEMPLATE, --template TEMPLATE
                        Meta-Task Template input (GraphXML File)
  -i IN_META, --in_meta IN_META
                        Meta-Task to be processed (GraphXML File)
  -o OUT_META, --out_meta OUT_META
                        Processed Meta-Task (GraphXML File)
  -p PURGE, --purge PURGE
                        Purge Meta-task from RDBMS, '0' means all
  -s, --store           Store Meta-Task in RDBMS
  -r RETRIEVE, --retrieve RETRIEVE
                        Retrieve Meta-Task from RDBMS
  -f FETCH, --fetch FETCH
                        Single Task to be fetched
  -T UPDATE_TASK, --update_task UPDATE_TASK
                        Update attributes of task(s)
  -D UPDATE_DATASET, --update_dataset UPDATE_DATASET
                        Update attributes of dataset(s)
  -x, --execute         Execute Meta-Task

  -N, --Ntimes          Allows to repeat the execution of the graph N times, for benchmarking

DEFT will require a short file containing the DB access info (credentials).
In addition, in its preliminary test version, it also needs a short file keeping
the current serial number for the database object, which serves to implement
autoincrement. This is subject to change.
