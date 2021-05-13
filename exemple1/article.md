# 


The state design pattern in computer science is intimitally related to the mathematical concept of Finite State Machine (FSM). The core concept is that you program will be composed of a series of step to perform, those step are formally called State. Within a given state the program will be performing some action and whenever some conditions, called transition, are match, the program will be transiting to a state and perform other action.

CI/CD heavily relies on state machine

GitOps approach relies on automated systems that ensure the configurations stored in source control (git for instance) are applied and in sync with the actual system. There is a lot of tool in the Open Source community that already offers that approached: Ansible, terraform, and, any ci/cd tools in general. On those tools, implement a finate state machine. Given a configuration file, execute a series of task to configure my environnment/infrastructure.

Then there is all those gab in the CI/CD/GitOps world where no tool cleary satisfy your companie's requirement. At that point in time you will be tinking: I am just going to create a simple python script that will solv my problem: call a couple api and setup everythng I need.

A naive approche would lead you to sequentially write code and implement the tasks you want to accomplished. The issue is that this way a creating a automation script is not flexible. An remember thet GitOps approach? You want you configuration to be in sync with the actual system, am I right? What if another team want to perform the same task? Can they use your script? What if there needs are slightly different? Are you goind to add a bunch of if else everywhere?

You may have gest it now. A better approach would be to create on configurable execution base on a State Machine. The big advantage of this approach is that is that you will focus on writting small (well tested) modules that performs a single task. On the side, you have a mechanism that execute those simple tasks base on a configuration file.

# Introduction to AsyncIO





