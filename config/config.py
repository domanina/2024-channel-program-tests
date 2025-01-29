import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_URL = os.environ.get("BASE_URL")
API_KEY = os.environ.get("API_KEY")

RDS_USERNAME = os.environ.get("RDS_USERNAME")
RDS_PASSWORD = os.environ.get("RDS_PASSWORD")
RDS_HOST = os.environ.get("RDS_HOST")
RDS_DATABASE_NAME = "db-test"

