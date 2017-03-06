# AWS Elastic Beanstalk - SciPy - SciKit - Flask Setup
Elastic Beanstalk (EB) relies on Amazon Linux AMIs (by default) to deploy our application. This AMI requires a few configuration tweaks to install SciPy and SciKit. These instructions ensure applications with SciPy and SciKit-Learn libraries startup properly on EB.

Topics:
* Need a small instance, not micro
* eb deploy --timeout to give SciPy time to compile

## Virtual Environments
In order to keep things clean, we will want to work with virtual environments. A minimum of two environments should be used:
1. Project Environment: A virtual environment containing python packages to run your code. Package requirements will be pulled from this environment, so make sure all dependencies are included!!!
> Note: The *boto* package is included in the standard EB image, and is optional to include in this environment.

2. EB CLI Environment: This is a simple environment containing only the *awsebcli* package to interface with the EB service.

## Application Directory
Your application directory requires the following assets in the root directory:
* application.py : The main python file for your program. In this example, it is our flask app file.
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

In the folder, create a *yuminstall.config* file containing the following commands:
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
│   └── yuminstall.config
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
> PARAMETER NOTE: The --instance_type parameter is optional. By default, EB will build a t2.micro (free) instance, but the compilation of the SciPy library requires more memory than t2.micro provides. We need a t2.small instance for this configuration.

> TROUBLESHOOTING: Occasionally, the first run through eb create will fail. Try again before diving into troubleshooting.

## Deploying Updates
When code and/or configurations are updated, the application can be updated easily with the following command:
```
(eb_cli_env)$ eb deploy
```
