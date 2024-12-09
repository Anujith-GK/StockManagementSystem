from autogen import AssistantAgent
import pandas as pd
import asyncio

# Load the Excel data
file_path = 'stock-sample 1.xlsx'
warehouse_df = pd.read_excel(file_path, sheet_name='warehouse')

# Clean and prepare the warehouse data
warehouse_cleaned = warehouse_df[['Warehouse ID', 'Location', 'SKU', 'Shipping Charge/unit/Km']].dropna()
# warehouse_cleaned = warehouse_cleaned.iloc[1:]  # Drop the header row
warehouse_cleaned.columns = ['Warehouse ID', 'Location', 'SKU', 'Shipping Charge/unit/Km']

# Order details
order_sku = "ELE-IPH14-001"
order_location = "Nashville, USA"
order_quantity = 20

# Prepare data to send to the Assistant Agent
warehouse_data = warehouse_cleaned.to_dict(orient="records")
order_data = {
    "Order SKU": order_sku,
    "Order Location": order_location,
    "Order Quantity": order_quantity,
}

# Define the Assistant Agent
class WarehouseAssistantAgent(AssistantAgent):
     def decide_best_warehouse(self, warehouse_data, order_data):
        # Create the reasoning prompt
        prompt = f"""
You are an assistant responsible for determining the best warehouse to fulfill an order.
Here is the problem:
1. The order location is "{order_data['Order Location']}" with a quantity of {order_data['Order Quantity']}.
2. Warehouse data includes:
{warehouse_data}

Steps to solve:
1. Filter out warehouses that has "{order_data['Order SKU']}" in their SKU.
2. Geocode the locations to find the latitude and longitude of each warehouse which is filter out in step 1 and the order location.
3. Calculate the distance between the order location and each warehouse.
4. Compute the shipping cost for each warehouse using the formula:
   Shipping Cost = Distance (km) × Shipping Charge/unit/km × Order Quantity.
5. Select the warehouse with the least shipping cost.
6. Return the Warehouse ID, location, distance, and total cost of the selected warehouse.

Perform all calculations and decisions based on the above data.I dont need any python code. Provide only the results.
"""
        # Call the model using the AssistantAgent's query method
        return self.generate_reply(messages=[{"content": prompt, "role": "user"}])
        # return self.generate_reply({'content':{'messages':prompt}})
    
llm_config = {"config_list": [
  {"model": "gpt-4o-mini", 
   "base_url": "https://oai-stock-search.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview", 
    "api_type": "azure",
    "api_key": "8S6mATWRVWLz5tux9nuCdhHmxOsverJ7YC4gEMohsOvsuVLkk2D4JQQJ99ALACYeBjFXJ3w3AAABACOGu8iG",
    "api_version": "2024-08-01-preview"}]
}
# Instantiate the Assistant Agent with a name and model configuration
assistant_agent = WarehouseAssistantAgent(
    name="WarehouseAgent",
    llm_config=llm_config
)


async def query_assistant_agent():
    decision = await asyncio.to_thread(assistant_agent.decide_best_warehouse, warehouse_data, order_data)
    print("Best Warehouse Decision:")
    print(decision)

asyncio.run(query_assistant_agent())







