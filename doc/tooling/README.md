# Tools used in the project
The following lists the tools and frameworks, that are used in the project. 
- [Docker](https://docs.docker.com/get-started/overview/)   
    Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker's methodologies for shipping, testing, and deploying code, you can significantly reduce the delay between writing code and running it in production.
- [Kubernetes](https://kubernetes.io/docs/concepts/overview/)  
    Kubernetes is an open-source system for automating deployment, scaling, and management of containerized applications.
    It groups containers that make up an application into logical units for easy management and scaling.
    Kubernetes helps orchestrate containerized applications across clusters of machines. 
- [FastAPI](https://fastapi.tiangolo.com/tutorial/)  
    FastAPI is a high-performance web framework for building APIs in Python.
    FastAPI simplifies the process of creating APIs with features like automatic data validation, background tasks, and dependency injection.

- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)  
    SQLAlchemy is an object-relational mapper (ORM) for Python that simplifies interaction with relational databases.
    It allows developers to define database schemas in Python classes and automatically translates between Python objects and database rows.
    SQLAlchemy reduces boilerplate code and simplifies database interaction.
- [FastAPI with SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/)  
    Combining FastAPI and SQLAlchemy is a powerful approach for building web applications with Python.
    FastAPI provides the framework for building the API, while SQLAlchemy handles database interactions.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)  
    Alembic is a database migration tool for SQLAlchemy.
    It helps manage schema changes in a database over time.
    Alembic allows developers to define database schema changes in migration scripts and automate their application.
- [Swagger UI](https://swagger.io/tools/swagger-ui/)  
    Swagger UI is a user interface for visualizing and interacting with RESTful APIs.
    It allows developers and users to explore API documentation, test endpoints, and understand how to interact with the API.
    By integrating Swagger UI with FastAPI, developers can easily provide interactive documentation for their APIs.

# GitLab CI/CD

The following is a collection of short hints on how to do the most essential things in a GitLab CI/CD pipeline:

- How to delay a job until another job is done: 

You can delay a job with the "needs" directive:  
```yaml
jobname:
  needs: 
    - job: <anotherjob>
```

- How to change the image used in a task: 

You can change the image used in a task with the "image" directive:  
```yaml
jobname:
  image: <myimage:mytag>
```

- How do you start a task manually:

```yaml
jobname:
  when: manual
```

- The Script part of the config file - what is it good for?

The script part defines the executed commands in the defined pipeline job

```yaml
jobname:
  script:
    - python -c "print('hello world')"
```

- If I want a task to run for every branch I put it into the stage ??

I put the job into the commit stage to run it in every branch.

```yaml
jobname:
  stage: commit
```

- If I want a task to run for every merge request I put it into the stage ??

I put the job into the acceptance (testing) stage to run it for every merge request.

```yaml
jobname:
  stage: acceptance
  only:
    - merge_requests
    - main
    - master
```

- If I want a task to run for every commit to the main branch I put it into the stage ??

I put the job into the release stage to run it for every commit on the main branch.

```yaml
jobname:
  stage: release
  only:
    - main
    - master
```

# flake8 / flakeheaven

- What is the purpose of flake8?

- What types of problems does it detect

- Why should you use a tool like flake8 in a serious project?

## Run flake8 on your local Computer

  It is very annoying (and takes a lot of time) to wait for the pipeline to check the syntax 
  of your code. To speed it up, you may run it locally like this:

### Configure PyCharm (only once)
- select _Settings->Tools->External Tools_ 
- select the +-sign (new Tool)
- enter Name: *Dockerflake8*
- enter Program: *docker*
- enter Arguments: 
    *exec -i 1337_pizza_web_dev flakeheaven lint /opt/project/app/api/ /opt/project/tests/*
- enter Working Directory: *$ProjectFileDir$*

If you like it convenient: Add a button for flake8 to your toolbar!
- right click into the taskbar (e.g. on one of the git icons) and select *Customize ToolBar*
- select the +-sign and Add Action
- select External Tools->Dockerflake8

### Run flake8 on your project
  - Remember! You will always need to run the docker container called *1337_pizza_web_dev* of your project, to do this! 
    So start the docker container(s) locally by running your project
  - Now you may run flake8 
      - by clicking on the new icon in your toolbar or 
      - by selecting from the menu: Tools->External Tools->Dockerflake8 

# GrayLog

- What is the purpose of GrayLog?

- What logging levels are available?

- What is the default logging level?

- Give 3-4 examples for logging commands in Python:
  ```python

  ```

# SonarQube

- What is the purpose of SonarQube?
  - Static Code Analysis / Finding Bugs: SonarQube helps in managing the quality of source code by performing static code analysis.
  It identifies bugs, vulnerabilities, and code smells in various programming languages.
  - Improving Maintainability: By highlighting issues, it aids developers in maintaining cleaner, more maintainable codebases.
  - Enhancing Security: It detects security vulnerabilities that could be exploited, thereby improving the security of the application.
  - Enforcing Coding Standards: SonarQube ensures that the code adheres to defined coding standards and best practices.


- What is the purpose of the quality rules of SonarQube?

  The quality rules of SonarQube serve as guidelines for code analysis and cover various aspects such as error detection, identification of security vulnerabilities, and elimination of code smells. 
  By automating the process of issue detection, quality rules help maintain consistency, improve overall code quality, and guide developers towards best practices. 
  The rules are defined by coding conventions (Python: PEP8).


- What is the purpose of the quality gates of SonarQube? 
  Quality gates in SonarQube serve as checkpoints that determine whether the code meets predefined quality criteria before integration into the main codebase. 
  They establish standards, prevent the accumulation of technical debt by halting the progression of low-quality code, and facilitate decisions by providing clear guidelines for code promotion or rejection. 
  Additionally, quality gates enable continuous quality improvement by ensuring consistent quality checks on all code changes and automating quality assurance processes for efficiency and consistency.


## Run SonarLint on your local Computer

It is very annoying (and takes a lot of time) to wait for the pipeline to run SonarQube. 
To speed it up, you may first run the linting part of SonarQube (SonarLint) locally like this:

### Configure PyCharm for SonarLint (only once)

- Open *Settings->Plugins*
- Choose *MarketPlace*
- Search for *SonarLint* and install the PlugIn

### Run SonarLint

- In the project view (usually to the left) you can run the SonarLint analysis by a right click on a file or a folder. 
  You will find the entry at the very bottom of the menu.
- To run it on all source code of your project select the folder called *app*

# VPN

The servers providing Graylog, SonarQube and your APIs are hidden behind the firewall of Hochschule Darmstadt.
From outside the university it can only be accessed when using a VPN.
https://its.h-da.io/stvpn-docs/de/ 