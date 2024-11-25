# CovidDataCollector

## 簡介
CovidDataCollector 是一個用於收集模擬疫情數據的服務，該服務使用 Python 開發，並基於 FastAPI 框架來實現 API 端點。該服務能夠接收、驗證、保存疫情相關的數據，以便進一步的處理和分析。

## 目錄結構
- **app**: 主應用程序的源代碼。
  - **api**: 定義 API 端點的邏輯。
  - **services**: 包含核心業務邏輯（如數據創建、驗證等）。
  - **handlers**: 包含異常處理邏輯。
  - **config**: 配置文件。
  - **exceptions**: 自定義的異常類型。
  - **main.py**: 服務啟動入口。

- **environments**: 各環境的配置文件。
  - **test/dev/prod**: 包含對應環境的 Dockerfile、依賴和環境變數文件。
  - **shared**: 通用的環境配置和資源。

- **README.md**: 本文件，提供項目基本信息和使用指南。

## 快速開始

1. **克隆專案**
   ```bash
   git clone <repository-url>
   cd CovidDataCollector
   ```

2. **選擇環境並構建 Docker 映像**
   - 開發環境：
     ```bash
     docker build -f environments/dev/Dockerfile.dev -t covid-data-collector:dev .
     ```
   - 測試環境：
     ```bash
     docker build -f environments/test/Dockerfile.test -t covid-data-collector:test .
     ```

3. **運行服務**
   ```bash
   docker run -p 8000:8000 covid-data-collector:dev
   ```

## 主要依賴
- Python 3.11
- FastAPI
- Docker
- SQLAlchemy Core