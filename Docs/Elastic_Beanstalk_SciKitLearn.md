# AWS Elastic Beanstalk - SciPy - SciKit - Flask Setup
Elastic Beanstalk is a PaaS solution that deploys web applications with load balancing, auto-scaling and monitoring features built-in. In this template, a SciKit-Learn model is deployed as a Flask API and hosted on Elastic Beanstalk (EB).

EB relies on Amazon Linux AMIs (based on RedHat) to deploy applications. This AMI requires a few configuration tweaks to install SciPy and SciKit. These instructions ensure applications with SciPy and SciKit-Learn libraries startup properly on EB.

## Intuition
As EB is auto-provisioning, the following instructions describe methods to package application code and configuration scripts in a way that can be consumed by the EB service to provision resources on demand.

All work described in this template is completed on a separate PC or EC2 instance. After preparing the EB package, a local command-line interface is used to initialize and launch the application on EB.

## Virtual Environments
In order to keep things clean, we will want to work with Python virtual environments. A minimum of two environments should be used:
1. Project Environment: A virtual environment containing python packages to run your code. Package requirements will be pulled from this environment, so make sure all dependencies are included!!!
> Note: The *boto* package is included in the standard EB image, and is optional to include in this environment.

2. EB CLI Environment: This is a simple environment containing only the *awsebcli* pip package to interface with the EB service for deployment.

## Application Directory
Your application directory requires the following assets in the root directory:
* application.py : The main python file for your program. In this example, it is our flask app file. Pay close attention to the application.py file in this example- EB specifically looks for application.py, any other name must be explicitly referenced in a WSGI config file (see *02_flask.config* example). In addition, our main Flask loop is called application.
* requirements.txt : A list of python dependencies, easily obtained with the command:
```
$ workon project_venv
(project_venv)$ pip3 freeze > requirements.txt
```
> WARNING: SciKit has a dependency on SciPy, but the SciKit installer will not automatically download the dependency. To ensure a reliable installation, manually move the SciKit line in your *requirements.txt* file below SciPy.

## Installing System Libraries
We need to add a yum configuration file to install system dependencies for SciPy. Without BLAS, LAPAC, Fortran and GCC compilers, SciPy will fail to install on this machine image and our Beanstalk fleet will fail to provision.

First, we need to add an *.ebextensions* folder to the root folder of your application.
```
$ mkdir .ebextensions
$ cd .ebextensions
```

In the folder, create a *01_yuminstall.config* file containing the following commands:
```
packages:
  yum:
    gcc-c++: []
    atlas-devel: []
    lapack-devel: []
    blas-devel: []
    libgfortran: []
```
When provisioning a machine, the Yum packages listed above will be installed.

At this stage, the minimum directory structure should be:
```
/app_folder/
├── .ebextensions
│   └── 01_yuminstall.config
├── application.py
└── requirements.txt
```

## WSGI configuration
The Web Server Gateway Interface (WSGI) that interfaces the application to the web has trouble when Python scripts call packages using C bindings, like NumPy. Python forces all C code to run under the first sub-process, but WSGI spins up multiple sub-processes by default. If we try to run code in a WSGI sub-process that is not running C, the process will deadlock. The configuration file *03_wsgi.config* will ensure that WSGI shares the first sub-process with C.
```
/app_folder/
├── .ebextensions
│   └── 01_yuminstall.config
│   └── 03_wsgi.config
├── application.py
└── requirements.txt
```

## Creating EB Application
Now that we are ready to create the application, switch over to the EB CLI virtual environment.
```
$ workon eb_cli_env
(eb_cli_env)$
```
Now we need to initialize the EB application
```
(eb_cli_env)$ eb init
```
You will be queried to chose a region, give a name to your new app, select a python version and asked to use SSH keys. Answer these carefully.

Init has generated an EB configuration file, but our application has not yet deployed. To deploy the application for the first time, we will use:
```
(eb_cli_env)$ eb create --instance_type t2.small --timeout 30
```
> PARAMETER NOTE: The --instance_type parameter is optional. By default, EB will build a t2.micro (free) instance, but the compilation of the SciPy library requires more memory than t2.micro provides. We need a t2.small instance for this configuration. A micro instance could be used with a swap file, but provisioning time is already long with a small instance and a swap file would extend the time even further.

> TROUBLESHOOTING: Be patient! The provisioning process will take ~30 minutes- during which time the health monitor will time out and show a degraded health state. Wait ~30 minutes to see whether health is restored before troubleshooting the EB package.

## Deploying Updates
When code and/or configurations are updated, the application can be updated easily with the following command:
```
(eb_cli_env)$ eb deploy
```
