# deft-archive
This repository contains the code of the initial version of the
"DEFT" component of the ATLAS Production System V2.0 (known as Prodsys2).
This project has since been superceded by a largely new and independent development.

# Tags: workflow, GraphML, XML, NetworkX

# Background and History
"DEFT" stands for "database engine for tasks".
The goal was to develop a simple and portable outer layer of a workflow management
system that could be used as a companion to ATLAS PanDA WMS.

Principal features of this version of "deft" are:
 * Reliance on DAG as the principal model of the workflow, represented as graphs
 * GraphML as the language for workflow (DAG) description
 * RDBMS as the storage back-end for graph storage
 * NetworkX package utilized to parse and manipulate DAGs


