import csv
import json
import random
import responses
from jinja2 import Template
from datetime import datetime, timedelta
from collections import defaultdict

from config.settings import API_URL, SERVER_IP, SERVER_PORT
from main import create_app


def mock_data_with_ratio(context, templates, population):
    tuples = []
    # ratio = false
    url = Template(templates[0]["url_template"]).render(context)
    response = Template(json.dumps(templates[0]["response_template"])).render(context)
    tuples.append((url, json.loads(response)))
    # ratio = true
    context["cases_population_ratio"] = round(
        context["aggregated_cases"] / population, 5
    )
    url = Template(templates[1]["url_template"]).render(context)
    response = Template(json.dumps(templates[1]["response_template"])).render(context)
    tuples.append((url, json.loads(response)))

    return tuples


def mock_request_and_response():
    # load templates
    with open("/test/cases/integration_test/templates.json", "r") as f:
        templates = json.load(f)
    # load templates for region, city, national
    region_templates = templates["region"]
    city_templates = templates["city"]
    national_templates = templates["national"]

    # load taiwan amdinistrative data
    with open("/app/utils/geo_data/administrative/taiwan_admin.json", "r") as f:
        tw_admin = json.load(f)
    # smaller data for testing
    # tw_admin = {
    #     "台北市": ["中正區", "大同區"],
    #     "高雄市": ["鳳山區"],
    #     "新北市": ["板橋區"],
    #     "台中市": ["西屯區"],
    #     "台南市": ["安南區"],
    #     "桃園市": ["桃園區"],
    #     "宜蘭縣": ["宜蘭市"],
    #     "新竹市": ["東區"],
    #     "苗栗縣": ["苗栗市"],
    #     "彰化縣": ["彰化市"],
    # }

    # load population data
    population = defaultdict(dict)
    with open("/app/utils/geo_data/population/region_population.csv", "r") as f:
        tw_population = csv.DictReader(f)
        next(tw_population, None)
        # build a dictionary for population
        for row in tw_population:
            population[row["COUNTY"]][row["TOWN"]] = int(row["P_CNT"])

    mock_tuples = []
    context = {"API_URL": API_URL, "now": datetime.today().strftime("%Y-%m-%d")}
    # in case interval = 1, 3, 7, these case for initial data
    for interval in ["1", "3", "7"]:
        context["interval"] = interval
        context["start_date"] = datetime.today() - timedelta(days=int(interval))
        context["start_date"] = context["start_date"].strftime("%Y-%m-%d")
        aggregate_by_national = 0
        # mock data for each city
        for city in tw_admin.keys():
            context["mock_city"] = city
            aggregate_by_city = 0
            city_population = 0
            # mock data for each region
            for region in tw_admin[city]:
                context["mock_region"] = region
                context["aggregated_cases"] = random.randint(0, 1000)
                region_population = population[context["mock_city"]][
                    context["mock_region"]
                ]
                mock_tuples.extend(
                    mock_data_with_ratio(context, region_templates, region_population)
                )
                city_population += region_population
                aggregate_by_city += context["aggregated_cases"]

            context["aggregated_cases"] = aggregate_by_city
            mock_tuples.extend(
                mock_data_with_ratio(context, city_templates, city_population)
            )
            aggregate_by_national += aggregate_by_city
        # mock data for national
        context["aggregated_cases"] = aggregate_by_national
        url = Template(national_templates["url_template"]).render(context)
        response = Template(json.dumps(national_templates["response_template"])).render(
            context
        )
        mock_tuples.append((url, json.loads(response)))

    # in case interval = 14, 30, without national
    for interval in ["14", "30"]:
        context["interval"] = interval
        context["start_date"] = datetime.today() - timedelta(days=int(interval))
        context["start_date"] = context["start_date"].strftime("%Y-%m-%d")
        aggregate_by_national = 0

        for city in tw_admin.keys():
            context["mock_city"] = city
            aggregate_by_city = 0
            city_population = 0
            # mock data for each region
            for region in tw_admin[city]:
                context["mock_region"] = region
                context["aggregated_cases"] = random.randint(0, 1000)
                region_population = population[context["mock_city"]][
                    context["mock_region"]
                ]
                mock_tuples.extend(
                    mock_data_with_ratio(context, region_templates, region_population)
                )
                city_population += region_population
                aggregate_by_city += context["aggregated_cases"]

            context["aggregated_cases"] = aggregate_by_city
            mock_tuples.extend(
                mock_data_with_ratio(context, city_templates, city_population)
            )
    return mock_tuples


@responses.activate
# @freeze_time("2023-06-07", ignore=["time"])
def manual_test():
    # Mock all requests to the analytics API
    for request, response in mock_request_and_response():
        responses.add(responses.GET, request, json=response, status=200)

    app = create_app()
    app.run_server(host=SERVER_IP, port=SERVER_PORT, debug=True)


if __name__ == "__main__":
    manual_test()
