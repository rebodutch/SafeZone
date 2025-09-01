# CovidDataSimulator

CovidDataSimulator is a service designed to simulate daily COVID-19 data, filter the generated data, and send it to a designated receiver service.
---

## **Features**
- Simulates daily or batch COVID-19 data.
- Filters data with customizable criteria (e.g., date).
- Sends the simulated data to a specified endpoint (e.g., CovidDataIngestor).

---

## **Requirements**
- Docker 24.0+

---

## **Configuration**

### **Environment Variables**
| Variable Name      | Default Value                     | Description                        |
|--------------------|-----------------------------------|------------------------------------|
| `ENVIRONMENT`      | `test`                           | The runtime mode (`test` or `production`). |
| `ACCEPTOR_URL`     | `http://localhost:8001/api/receive` | The URL of the receiver service.  |

---

## **Setup Guide**
