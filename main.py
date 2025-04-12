import requests
import json
import os

MOCKAROO_API_KEY = os.environ.get("MOCKAROO_API_KEY")
print(MOCKAROO_API_KEY)
MOCKAROO_API_URL = "https://api.mockaroo.com/api"

def generate_mockaroo_data(config_json):
    results = {}
    for schema_def in config_json.get("schemas", []):
        schema_name = schema_def.get("schema_name")
        record_count = schema_def.get("record_count", 10)
        schema = schema_def.get("schema")
        
        if schema:
            print(f"Generating {record_count} records for custom schema: {schema_name}")
            response = requests.post(
                f"{MOCKAROO_API_URL}/generate.json?key={MOCKAROO_API_KEY}&count={record_count}",
                headers={"Content-Type": "application/json"},
                data=json.dumps(schema)
            )
        else:
            print(f"Fetching {record_count} records from saved schema: {schema_name}")
            response = requests.get(
                f"{MOCKAROO_API_URL}/{schema_name}.json?key={MOCKAROO_API_KEY}&count={record_count}"
            )
        
        if response.status_code == 200:
            results[schema_name] = response.json()
        else:
            print(f"Error for schema {schema_name}: {response.status_code} - {response.text}")
            results[schema_name] = {"error": response.text}
    
    return results


# Sample JSON Inputs
# Example 1: users and orders with reference
c1 = {
  "schemas": [
    {
      "schema_name": "users",
      "record_count": 5,
      "schema": [
        { "name": "id", "type": "Row Number" },
        { "name": "first_name", "type": "First Name" },
        { "name": "email", "type": "Email Address" }
      ]
    },
    {
      "schema_name": "orders",
      "record_count": 10,
      "schema": [
        { "name": "order_id", "type": "Row Number" },
        {
            "name": "user_id",
            "type": "Dataset Column",
            "dataset": "users",
            "column": "id",
        #   "type": "Reference",
        #   "referencedSchema": "users",
        #   "referencedField": "id"
        },
        { "name": "product", "type": "Product (Grocery)" }
      ]
    }
  ]
}


# Example 2: companies and employees with cross reference
c2 = {
  "schemas": [
    {
      "schema_name": "companies",
      "record_count": 3,
      "schema": [
        { "name": "company_id", "type": "Row Number" },
        { "name": "company_name", "type": "Company Name" }
      ]
    },
    {
      "schema_name": "employees",
      "record_count": 6,
      "schema": [
        { "name": "emp_id", "type": "Row Number" },
        {
            "name": "company_id",
            "type": "Dataset Column",
            "dataset": "companies",
            "column": "company_id",
        #   "type": "Reference",
        #   "referencedSchema": "companies",
        #   "referencedField": "company_id"
        },
        { "name": "name", "type": "Full Name" }
      ]
    }
  ]
}

# Example 3: No schema, fetch from saved schema customers
c3 = {
  "schemas": [
    {
    #   "schema_name": "customers",
      "schema_name": "91a933e0",
      "record_count": 5
    }
  ]
}



if __name__ == "__main__":
    print("Generating mockaroo data...")
    schemas = [c1, c2, c3]
    for schema in schemas:
        print(generate_mockaroo_data(schema), "\n\n")