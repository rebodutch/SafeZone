import plotly.graph_objs as go
import dash
import json
from dash import dcc, html

# 建立 Dash 應用
app = dash.Dash(__name__)

# 加載 GeoJSON 文件，這個文件包含台灣各鄉鎮市區的邊界
with open("app/utils/geo_data/towns_updated.json", "r") as f:
    geojson_data = json.load(f)

# 模擬風險數據，確保名稱完全一致
with open("app/assets/coloring_data.json", "r") as f:
    region_risk = json.load(f)

# 建立 Choroplethmapbox 圖形
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson_data,
    locations=list(region_risk.keys()),  # 與 GeoJSON 中的區域屬性匹配
    featureidkey="properties.FULLNAME",  # 對應 GeoJSON 中的區域名稱屬性
    z=list(region_risk.values()),        # 風險等級數據
    colorscale="Reds",                   # 使用顏色比例 Reds，更容易區分風險
    marker_opacity=0.9,                  # 調高透明度，顯示更明顯
    marker_line_width=1
))

# 設定地圖屬性，將地圖居中於新店區
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=12,                      # 提高縮放級別來聚焦
    mapbox_center={"lat": 24.9713, "lon": 121.5394}  # 新店區的中心經緯度
)

# 定義應用佈局
app.layout = html.Div([
    html.H1("SafeZone 疫情風險儀表板"),
    dcc.Graph(id="map", figure=fig)
])

# 運行應用程序
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)