# Medifax Employee Portal

This application is a light-weight frontend build on Flask that utilizes AWS Lambda functions as the middleware layer.

## Running the Application

To start the application in local development/debug mode, execute the following commands in your local terminal:

```bash
export FLASK_APP=application.py
export FLASK_DEBUG=1
flask run```

## Production Environment



## Deploying the Application

## PROD DEPLOYMENT CHECKLIST

1) Update AWS keys in `routes.py`. These are used by `tinys3` for image management to S3.
