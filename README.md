# Group-Stierna
Repository for Group Stierna in the development of a platooning system for the MOPED.

[MOPED Github repository](https://github.com/sics-sse/moped)

This repository contains two parts; an "onMoped" python3-package that's run on the MOPED and an Android-app for remote control. 

**The onMoped** package is mostly self-serving, but requires [can-utils](https://github.com/linux-can/can-utils) to communicate with the other ECU:s on the MOPED.


Documentation related to the assignment, such as sprint retrospectives and code reviews can be found on the [documentation branch](https://github.com/petrosdeb/Group-Stierna/tree/documentation)

`/StiernaController` contains the source code for the Android-app that can control the MOPED over local network.

`/onMoped/control` contains most of the relevant code running on the MOPED. It needs to be initiated with `run.py`.

`/legacy` contains ancient code from the original MOPED repository, on which the communication over the CAN is based. It is kept mostly for posterity.

[Trello Backlog](https://trello.com/b/THHlHSP9) 
**TODO move this to documentation**
