# SafeZone Analytics API

SafeZoneAnalyticsAPI 提供高效的數據分析服務，支持多條件查詢和數據處理，滿足疫情數據分析需求。

---

## 功能概述

1. **查詢功能**

   - 支持按地區、時間範圍和案例類型進行數據查詢。
   - 提供結構化的查詢結果，包括病例總數和增長率。

2. **數據類型支持**

   - 支持按案例個數或人口比例進行數據查詢和分析。

---

## 目錄架構

```plaintext
SafeZoneAnalyticsAPI/
├── app/                   # 主應用邏輯與功能模組
│   ├── api/               # API 端點與數據模式
│   ├── config/            # 環境與日誌配置
│   ├── exceptions/        # 異常處理模組
│   ├── pipeline/          # 數據處理與分析管道
│   ├── main.py            # 主程序入口
├── environments/          # 環境配置
│   ├── dev/               # 開發環境
│   ├── prod/              # 生產環境
│   ├── test/              # 測試環境與數據
├── .env                   # 環境變數配置
├── Dockerfile.test        # 測試環境 Docker 配置
├── requirements.txt       # 項目依賴
└── README.md              # 項目說明文檔
```

---

## RESTful API 範例

以下是 SafeZone Analytics API 的主要端點及其使用範例：

### 1. **區域數據查詢**

**端點**:
```
GET /cases/region
```
**請求參數**:
| 參數名稱       | 類型     | 必填  | 描述                           |
|----------------|----------|-------|--------------------------------|
| `now`          | `string` | 是    | 當前日期，格式為 `YYYY-MM-DD` |
| `interval`     | `int`    | 是    | 查詢的日期範圍天數，例如 `7`   |
| `city`         | `string` | 是    | 城市名稱                       |
| `region`       | `string` | 是    | 區域名稱                       |
| `ratio`        | `bool`   | 否    | 是否返回人口比例數據           |

**回應範例**:
```json
{
    "data": {
        "start_date": "2023-01-01",
        "end_date": "2023-01-07",
        "city": "Taipei",
        "region": "Xinyi",
        "aggregated_cases": 150
    },
    "message": "Data returned successfully",
    "detail": "Data returned successfully for dates 2023-01-01 ~ 2023-01-07.",
    "success": true
}
```

### 2. **城市數據查詢**

**端點**:
```
GET /cases/city
```
**請求參數**:
| 參數名稱       | 類型     | 必填  | 描述                           |
|----------------|----------|-------|--------------------------------|
| `now`          | `string` | 是    | 當前日期，格式為 `YYYY-MM-DD` |
| `interval`     | `int`    | 是    | 查詢的日期範圍天數，例如 `7`   |
| `city`         | `string` | 是    | 城市名稱                       |
| `ratio`        | `bool`   | 否    | 是否返回人口比例數據           |

**回應範例**:
```json
{
    "data": {
        "start_date": "2023-01-01",
        "end_date": "2023-01-07",
        "city": "Taipei",
        "aggregated_cases": 500
    },
    "message": "Data returned successfully",
    "detail": "Data returned successfully for dates 2023-01-01 ~ 2023-01-07.",
    "success": true
}
```

### 3. **全國數據查詢**

**端點**:
```
GET /cases/national
```
**請求參數**:
| 參數名稱       | 類型     | 必填  | 描述                           |
|----------------|----------|-------|--------------------------------|
| `now`          | `string` | 是    | 當前日期，格式為 `YYYY-MM-DD` |
| `interval`     | `int`    | 是    | 查詢的日期範圍天數，例如 `7`   |

**回應範例**:
```json
{
    "data": {
        "start_date": "2023-01-01",
        "end_date": "2023-01-07",
        "aggregated_cases": 10000
    },
    "message": "Data returned successfully",
    "detail": "Data returned successfully for dates 2023-01-01 ~ 2023-01-07.",
    "success": true
}
```

---

