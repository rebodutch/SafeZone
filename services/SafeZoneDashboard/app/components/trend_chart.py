from dash import html
from services.update_cases import get_city_data
# test data
# data = [
#     {"city": "台北市", "cases": 120},
#     {"city": "新北市", "cases": 110},
#     {"city": "台中市", "cases": 95},
#     {"city": "高雄市", "cases": 80},
#     {"city": "台南市", "cases": 75},
#     {"city": "桃園市", "cases": 65},
#     {"city": "彰化縣", "cases": 55},
#     {"city": "新竹市", "cases": 50},
#     {"city": "宜蘭縣", "cases": 45},
#     {"city": "基隆市", "cases": 40},
# ]

# max_cases = max([item["cases"] for item in data]) 


def create_table():
    # get the data
    data = get_city_data("7")
    # get the max cases
    # print(type(data), data)
    max_cases = max([v for k,v in data.items()]) 
    # get top 10 cases growth cities
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    # get the top 10 cities
    data = [{"city": city, "cases": cases} for city, cases in sorted_data[:10]]

    rows = []
    # add the header of the table
    rows.append(
        html.Tr(
            [
                 # set the column width to 20%
                html.Th("City", style={"width": "20%"}), 
                 # set the column width to 80%
                html.Th("Cases", style={"width": "80%"}),
            ]
        )
    )

    # add the data rows
    for item in data:
        # calculate the width of the bar
        bar_width = (item["cases"] / max_cases) * 100 * 0.8
        # calculate the opacity of the bar
        bar_opacity = item["cases"] / max_cases
        rows.append(
            html.Tr(
                [
                    html.Td(item["city"], style={"width": "20%"}),
                    html.Td(
                        [
                            # display the number of cases
                            html.P(
                                item["cases"],
                                style={
                                    "width": "20%",  
                                    "textAlign": "right",  
                                    # make sure the number is in the middle of the bar
                                    "margin": "0",  
                                    # set the margin between the number and the bar
                                    "marginRight": "10px", 
                                },
                            ),
                            # display the bar
                            html.Div(
                                style={
                                    # set the width of the bar
                                    "width": f"{bar_width}%",
                                    "height": "20px",
                                    # set the gradient color of the bar
                                    "backgroundColor": f"rgba(0, 51, 153, {bar_opacity})",
                                    # set the border radius to make the bar looks like a pill
                                    "borderRadius": "5px",
                                }
                            ),
                        ],
                        style={
                            # make the number and the bar in the same line
                            "display": "flex",  
                            "alignItems": "center",
                            "width": "100%",  
                        },
                    ),
                ],
            )
        )
    return rows


def get_trend_bar():
    return html.Div(
        html.Table(
            create_table(),
            style={
                "textAlign": "center",
                "width": "100%",
                "margin": "auto",
            },
        ),
    )
