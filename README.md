# Overview 

This is a project on predicting Data Science and STEM Salaries. This is done as part of the Machine Learning Engineering course held by Alexey Grigorev.
Credits to Jack Ogozaly for scraping the dataset from level.fyi!
If you want to see the original dataset on kaggle, look at it here: [Dataset](https://www.kaggle.com/jackogozaly/data-science-and-stem-salaries)


## Problem description

There is a lot of variation with regards to Data Science and STEM salaries, ranging from the location that one is based in, to the company one is based in.
Moreover, it is not very convenient to find this information on the internet, with some platforms gatekeeping information about salary.
Therefore, this model takes these variables and conveniently predicts the salary that you'll receive with said variables.

## Contents of the folder 

The data folder consists of the original dataset, as well as the cleaned dataset.

The code folder consists of: 
<ul>
<li> Data Cleaning & EDA - part of the notebook </li>
<li> Training of model & Hyperparameter Tuning (output & outputless)* - part of notebook </li>
<li> train.py - to train the final model + saving it using pickle </li>
<li> predict.py - to load the model and serve it via a web service </li>
<li> predict-test.py and predict-test-cloud.py - to test the output of the model, depending on where you want to use it </li>
<li> pipenv and pipenv.lock for the virtunal environment using pipenv </li>
<li> Dockerfile for using a Docker container </li>
<li> requirements.txt and Procfile for Heroku deployment </li> 
</ul>

as well as some files that logs the training process (catboostinfo), some files for deplyoing the model to the cloud using AWS Elastic Beanstalk and some notebook checkpoints.

*= second notebook had problems loading on github, and part of it is due to the output from the notebook. Therefore, I have decided to include both copies. Do note that the notebook with the output WILL lag, so it is up to your own discretion to download it. It is, however, still there.
  

## Deployment of model

I am currently using Windows, so I am using waitress in order to deploy the model.
To deploy this model with waitress, please use: waitress-serve --listen=0.0.0.0:9696 predict:app

## Virtual Environment/venv 

I used pipenv for the virtual environment. In order to use the same venv as me, do use pip install pipenv.

To replicate the environment, on your command line, use pipenv install numpy scikit-learn==0.24.2 catboost flask gunicorn waitress

Do note that catboost takes longer than the other modules to install. 

(For reference, catboost took about a minute or two on my computer, the rest took about 10 seconds) 

You can run the environment using pipenv shell, and deploy the model as normal.

To deploy the model, refer to the "Depolyment of model" part of the README.

## Docker

I have built the model and pushed it to [kwangyy/salary-prediction:3.8.12-slim](https://hub.docker.com/r/kwangyy/salary-prediction) for easy use!

To take the model from the docker container I built, just replace
`FROM python:3.8.12-slim` with 
`FROM kwangyy/salary-prediction:3.8.12` in the dockerfile.

If you choose to build a docker file locally instead, here are the steps to do so:
1. In your command line, run: `docker run -it --rm --entrypoint=bash python:3.8.12-slim` to create a docker image.

2. Create a Dockerfile as such:

~~~~
FROM python:3.8.12-slim

RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict.py", "catboostreg.bin", "./"]

EXPOSE 9696

ENTRYPOINT ["waitress-serve", "--listen=0.0.0.0:9696", "predict:app"]
~~~~

This allows us to install python, run pipenv and its dependencies, run our predict script and our model itself and deploys our model using waitress.
Similarly, you can just use the dockerfile in this repository.

3. Build the docker container with `Docker built -t salary-prediction . `

4. Run the docker container with `Docker run -it -p 9696:9696 salary-prediction:latest` so that we can use our model!

## Deploying onto AWS Elastic Beanstalk
To deploy this into the cloud using AWS Elastic Beanstalk: 
1. Use `pipenv install --dev awsebcli` to install the command line for AWS Elastic Beanstalk. This is because we only need Elastic Beanstalk for deploying to the cloud and not actually for the model itself. 
2. Use `eb local run --port 9696`, allowing EB to build the Docker container.
3. Use `eb create salary-serving-env` to create the environment for the container itself 
4. AWS will start creating the environment, so do give it a few minutes. Once it is done, there will be a line that says 'Application available at ....'. Copy and paste the link - that is your new host. 
5. If you happen to use a .py file for a request, do change your host to the link, and your url to a f-string.
e.g. If your host = `kwangyy.importantletters.us-east-2.elasticbeanstalk.com`, then your url = `f'http://{host}/predict'`
6. To terminate, use `eb terminate salary-serving-env` to not waste your EC2 hours (you need to pay for your instance hours once it hits a certain limit, you know that right?) 

## If you like the project, it would be appreciated if you star this repo. Please feel free to fork the content as well!
[Kaggle](https://www.kaggle.com/kwangyangchia)

[Linkedin](https://www.linkedin.com/in/kwang-yang-chia/)
