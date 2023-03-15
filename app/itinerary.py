import os
from datetime import date, timedelta

import requests
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

import app
from app import openai


class MaxDaysValidator(object):
    def __init__(self, max_days):
        self.max_days = max_days

    def __call__(self, form, field):
        start_date = form.start_date.data
        end_date = field.data

        if end_date - start_date > timedelta(days=self.max_days):
            raise ValidationError(f"Duration cannot exceed {self.max_days} days.")


class EndDateValidator(object):
    def __call__(self, form, field):
        start_date = form.start_date.data
        end_date = field.data

        if end_date < start_date:
            raise ValidationError("End date cannot be before the start date.")


class DestinationValidator(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, form, field):
        query = field.data
        print(f"API Key: {self.api_key}")  # Debugging: print the API key
        url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={query}&inputtype=textquery&key={self.api_key}"
        print(url)
        response = requests.get(url)
        data = response.json()
        print(f"Response Data: {data}")  # Debugging: print the response data

        if data["status"] != "OK":
            raise ValidationError("Invalid destination. Please enter a valid location.")


class ItineraryForm(FlaskForm):
    destination = StringField(
        "Destination",
        validators=[
            DataRequired(),
            DestinationValidator(os.getenv("GOOGLE_PLACES_API_KEY")),
        ],
    )
    start_date = DateField("Start Date", format="%Y-%m-%d", validators=[DataRequired()])
    end_date = DateField(
        "End Date",
        format="%Y-%m-%d",
        validators=[DataRequired(), EndDateValidator(), MaxDaysValidator(10)],
    )
    interests = TextAreaField("Interests")  # Removed DataRequired() validator
    submit = SubmitField("Create Itinerary")


def generate_itinerary(destination, start_date, end_date, interests):
    end_date = min(end_date, start_date + timedelta(days=9))
    number_of_days = (end_date - start_date).days + 1

    user_input = "\n".join(
        [
            "UserInput",
            f"CurrentDate:{date.today()}",
            f"Destination:{destination}",
            f"StartDate:{start_date}",
            f"EndDate:{min(end_date, start_date + timedelta(days=4))}",
            f"Days:{min(number_of_days, 5)}",
            f"Interests:{str(interests)}",
            "VacaBot",
        ]
    )

    with open("app/prompts/itinerary.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    prompt = f"{prompt}\n{user_input}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    itinerary = response.choices[0].text.strip()
    if number_of_days > 5:
        itinerary = itinerary + "\n### Day 6:"
        user_input = "\n".join(
            [
                "UserInput",
                f"CurrentDate:{date.today()}",
                f"Destination:{destination}",
                f"StartDate:{start_date}",
                f"EndDate:{end_date}",
                f"Days:{number_of_days}",
                f"Interests:{str(interests)}",
                "VacaBot",
                itinerary,
            ]
        )
        with open("app/prompts/itinerary2.txt", "r", encoding="utf-8") as f:
            prompt = f.read()
        prompt = f"{prompt}\n{user_input}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=3000,
            n=1,
            stop=None,
            temperature=0.7,
        )
        itinerary2 = response.choices[0].text.strip()
        itinerary = "\n".join([itinerary, itinerary2])
    return itinerary
