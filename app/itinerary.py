import os
from datetime import date, timedelta

import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")


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

        print("2------------")
        print(prompt)

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=3000,
            n=1,
            stop=None,
            temperature=0.7,
        )
        print("2------------")
        print(response)
        itinerary2 = response.choices[0].text.strip()
        itinerary = "\n".join([itinerary, itinerary2])
    return itinerary
