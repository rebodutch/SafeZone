import json
from unittest.mock import patch

from main import create_app

@patch("components.card.get_national_cases")
@patch("components.map_chart.get_city_data")
@patch("components.trend_chart.get_city_data")
@patch("callbacks.risk_map_callbacks.get_region_data")
@patch("callbacks.risk_map_callbacks.get_city_data")
def manual_test(mock_risk_city_data, mock_risk_region_data, mock_trend_city_data, mock_chart_city_data, mock_card_cases):
    with open("/test/cases/manual_test/mock_data.json", "r") as f:
        mock_services = json.load(f)
    # mock the return value of the services.update.get_city_data function
    mock_risk_city_data.return_value = mock_services["get_city_data"]
    mock_risk_region_data.return_value = mock_services["get_region_data"]
    mock_trend_city_data.return_value = mock_services["get_city_data"]
    mock_chart_city_data.return_value = mock_services["get_city_data"]
    mock_card_cases.return_value = mock_services["get_national_cases"]
   
    app = create_app()
    app.run_server(host="0.0.0.0", debug=True)

if __name__ == "__main__":
    manual_test()