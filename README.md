# Django CI/CD Pipeline with GitHub, AWS CodePipeline, CodeBuild, and Elastic Beanstalk

This repository contains a Django project configured for continuous integration and continuous deployment using GitHub, AWS CodePipeline, AWS CodeBuild, and AWS Elastic Beanstalk.

## Project Structure

```
.
├── .ebextensions/           # Elastic Beanstalk configuration
│   └── django.config        # Django-specific EB configuration
├── mysite/                  # Django project
├── buildspec.yml            # AWS CodeBuild specification
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Setup Instructions

### 1. GitHub Repository Setup

1. Create a new GitHub repository
2. Clone the repository to your local machine or AWS Cloud9 environment
   ```
   git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   ```
3. Add your Django project files to the repository
4. Push your changes to GitHub
   ```
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

### 2. AWS Elastic Beanstalk Setup

1. Install the EB CLI:
   ```
   pip install awsebcli --upgrade --user
   ```

2. Initialize your EB application:
   ```
   eb init -r eu-west-1 -p python-3.9 YOUR-APPLICATION-NAME
   ```

3. Create an EB environment:
   ```
   eb create YOUR-APPLICATION-NAME-env
   ```

### 3. AWS CodePipeline Setup

1. Open the AWS Management Console and navigate to CodePipeline
2. Click "Create pipeline"
3. Enter a pipeline name and select "Existing service role"
4. Choose "GitHub (Version 2)" as the source provider
5. Connect to your GitHub repository and select the main branch
6. Skip the build stage (we'll add it later)
7. Add a deploy stage with AWS Elastic Beanstalk as the provider
8. Select your application and environment created in step 2
9. Review and create the pipeline

### 4. Add AWS CodeBuild to Your Pipeline

1. Edit your pipeline in the AWS CodePipeline console
2. Add a build stage after the source stage
3. Select AWS CodeBuild as the build provider
4. Create a new build project:
   - Use the buildspec.yml file in your repository
   - Select an appropriate compute environment
   - Configure environment variables if needed
5. Save your changes

## How It Works

1. When you push changes to your GitHub repository, AWS CodePipeline automatically detects the changes
2. The source stage pulls the latest code from GitHub
3. CodeBuild builds your application according to the buildspec.yml file
4. If the build is successful, the application is deployed to Elastic Beanstalk
5. Elastic Beanstalk handles the deployment and scaling of your Django application

## Important Configuration Files

### .ebextensions/django.config

This file tells Elastic Beanstalk how to run your Django application:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: mysite.wsgi:application
  aws:elasticbeanstalk:environment:proxy:staticfiles:
    /static: static
```

### buildspec.yml

This file tells CodeBuild how to build your application:

```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.9
    commands:
      - echo Installing dependencies...
      - pip install -r requirements.txt
  
  pre_build:
    commands:
      - echo Running tests...
      - python -m pytest || true
      - echo Running linting...
      - flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
  
  build:
    commands:
      - echo Build started on `date`
      - echo Collecting static files...
      - python manage.py collectstatic --noinput || true
  
  post_build:
    commands:
      - echo Build completed on `date`

artifacts:
  files:
    - '**/*'
  base-directory: '.'
```

## Best Practices

1. Always use a virtual environment for local development
2. Keep your requirements.txt file updated
3. Write tests for your application
4. Use environment variables for sensitive information
5. Monitor your application using AWS CloudWatch
6. Set up proper IAM roles and permissions for security
