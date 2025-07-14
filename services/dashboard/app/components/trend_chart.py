from dash import html # type: ignore
from services.update_cases import get_city_data


def create_table(date):
    # get the data
    data = get_city_data(date, "7")
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
        bar_width = (item["cases"] / max_cases) * 100 * 0.8 if max_cases > 0 else 0
        # calculate the opacity of the bar
        bar_opacity = item["cases"] / max_cases if max_cases > 0 else 0
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


def get_trend_bar(date):
    return html.Div(
        html.Table(
            create_table(date),
            style={
                "textAlign": "center",
                "width": "100%",
                "margin": "auto",
            },
        ),
    )
