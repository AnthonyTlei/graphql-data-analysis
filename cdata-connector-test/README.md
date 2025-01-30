# CData Connector Test Project

## Overview
This project tests the **CData Python Connector for GraphQL** by:
- Connecting to a public **GraphQL API** (Countries API: https://countries.trevorblades.com/).
- Querying the API using **SQL syntax** via the **CData Python Connector**.
- Fetching results and storing them in a **Pandas DataFrame**.

## Prerequisites
- **Ubuntu** or another Linux distribution
- **Python 3.12** (or compatible version)
- **CData Python Connector for GraphQL** (Licensed or Trial)
- **Virtual environment (venv)** for isolation

## Installation Steps
### 1️⃣ Download the CData Python Connector for GraphQL
- Go to [CData’s official site](https://www.cdata.com/drivers/graphql/python/) and download the connector for Linux.
- Move it to a dedicated directory:
  ```bash
  mkdir -p ~/dev/tools/cdata
  mv ~/Downloads/CDataGraphQLPython.zip ~/dev/tools/cdata/
  cd ~/dev/tools/cdata/
  unzip CDataGraphQLPython.zip
  ```

### 2️⃣ Create and Activate a Virtual Environment
Navigate to the project directory and create a **virtual environment**:
```bash
cd ~/dev/graphql-data-analysis/cdata-connector-test
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install CData Connector in the Virtual Environment
Find and install the `.tar.gz` package:
```bash
pip install ~/dev/tools/cdata/CData.Python.GraphQL/unix/cdata-graphql-connector-24.0.9111-python3.tar.gz
```
Verify installation:
```bash
python -c "import cdata.graphql as graphql; print(graphql.__name__)"
```

### 4️⃣ Activate the License
To activate a **trial** or full **license**:
```bash
~/dev/graphql-data-analysis/cdata-connector-test/venv/lib/python3.12/site-packages/cdata/installlic_graphql/install-license.sh
```
If using a full license, replace `<your-key>`:
```bash
~/dev/graphql-data-analysis/cdata-connector-test/venv/lib/python3.12/site-packages/cdata/installlic_graphql/install-license.sh <your-key>
```

### 5️⃣ Run the Test Script
```bash
python src/test_cdata.py
```

### Expected Output
A Pandas DataFrame with country capitals, codes, and continent names:
```
         capital code continent_name
0     Algiers    DZ   Africa
1     Luanda     AO   Africa
2     Porto Novo BJ   Africa
...
```

---

## **requirements.txt**
To replicate this setup, install dependencies with:
```bash
pip install -r requirements.txt
```

---

## **Troubleshooting**
### **Common Errors and Fixes**
#### 1️⃣ `../jre/bin/java: not found`
- Ensure Java is installed:
  ```bash
  sudo apt install -y openjdk-11-jre
  ```
- Modify the `install-license.sh` script to use system Java.

---

---
.

**Author:** Anthony Tleiji

**Date:** Jan 30 2025

