# from autogen import AssistantAgent
# import json

# # JSON data for the warehouses
# warehouses_json = '''
# [
#     {
#         "id": 1,
#         "name": "Warehouse Alpha",
#         "location": "New York, NY",
#         "shipping_cost_per_km": 1.5,
#         "distance_to_customer_km": 120
#     },
#     {
#         "id": 2,
#         "name": "Warehouse Bravo",
#         "location": "Los Angeles, CA",
#         "shipping_cost_per_km": 2.0,
#         "distance_to_customer_km": 300
#     },
#     {
#         "id": 3,
#         "name": "Warehouse Charlie",
#         "location": "Chicago, IL",
#         "shipping_cost_per_km": 1.8,
#         "distance_to_customer_km": 250
#     },
#     {
#         "id": 4,
#         "name": "Warehouse Delta",
#         "location": "Houston, TX",
#         "shipping_cost_per_km": 1.6,
#         "distance_to_customer_km": 400
#     },
#     {
#         "id": 5,
#         "name": "Warehouse Echo",
#         "location": "Phoenix, AZ",
#         "shipping_cost_per_km": 2.2,
#         "distance_to_customer_km": 350
#     },
#     {
#         "id": 6,
#         "name": "Warehouse Foxtrot",
#         "location": "Philadelphia, PA",
#         "shipping_cost_per_km": 1.7,
#         "distance_to_customer_km": 100
#     },
#     {
#         "id": 7,
#         "name": "Warehouse Golf",
#         "location": "San Antonio, TX",
#         "shipping_cost_per_km": 1.9,
#         "distance_to_customer_km": 500
#     },
#     {
#         "id": 8,
#         "name": "Warehouse Hotel",
#         "location": "San Diego, CA",
#         "shipping_cost_per_km": 2.1,
#         "distance_to_customer_km": 275
#     },
#     {
#         "id": 9,
#         "name": "Warehouse India",
#         "location": "Dallas, TX",
#         "shipping_cost_per_km": 1.8,
#         "distance_to_customer_km": 325
#     },
#     {
#         "id": 10,
#         "name": "Warehouse Juliet",
#         "location": "San Jose, CA",
#         "shipping_cost_per_km": 2.3,
#         "distance_to_customer_km": 150
#     }
# ]
# '''

# # Parse the JSON data
# warehouses = json.loads(warehouses_json)

# # Order quantity
# order_quantity = 20

# # Create a Custom Agent Class
# class WarehouseAssistantAgent(AssistantAgent):
#     def calculate_total_cost(self, warehouse, quantity):
#         """
#         Calculates the total shipping cost for a warehouse based on order quantity.
#         """
#         total_cost = warehouse["shipping_cost_per_km"] * warehouse["distance_to_customer_km"] * quantity
#         return total_cost

#     def decide_best_warehouses(self, warehouses, quantity):
#         """
#         Returns a sorted list of warehouses with total costs in ascending order.
#         """
#         warehouse_costs = []

#         for warehouse in warehouses:
#             total_cost = self.calculate_total_cost(warehouse, quantity)
#             warehouse["total_cost"] = total_cost
#             warehouse_costs.append(warehouse)

#         # Sort warehouses by total cost
#         sorted_warehouses = sorted(warehouse_costs, key=lambda w: w["total_cost"])
#         return sorted_warehouses

# # Instantiate the Custom Agent
# agent = WarehouseAssistantAgent(name="WarehouseAI", description="Find the best warehouse based on shipping costs.")

# # Run the agent to find and sort warehouses by shipping cost
# if __name__ == "__main__":
#     sorted_warehouses = agent.decide_best_warehouses(warehouses, order_quantity)

#     print("Warehouses sorted by total shipping cost:")
#     for idx, warehouse in enumerate(sorted_warehouses, start=1):
#         print(f"{idx}. Name: {warehouse['name']}, Location: {warehouse['location']}, Total Cost: ${warehouse['total_cost']:.2f}")


from autogen import AssistantAgent
import json
import asyncio

# JSON data for the warehouses
warehouses_json = '''
[
    {
        "id": 1,
        "name": "Warehouse Alpha",
        "location": "New York, NY",
        "shipping_cost_per_km": 1.5,
        "distance_to_customer_km": 120
    },
    {
        "id": 2,
        "name": "Warehouse Bravo",
        "location": "Los Angeles, CA",
        "shipping_cost_per_km": 2.0,
        "distance_to_customer_km": 300
    },
    {
        "id": 3,
        "name": "Warehouse Charlie",
        "location": "Chicago, IL",
        "shipping_cost_per_km": 1.8,
        "distance_to_customer_km": 250
    },
    {
        "id": 4,
        "name": "Warehouse Delta",
        "location": "Houston, TX",
        "shipping_cost_per_km": 1.6,
        "distance_to_customer_km": 400
    },
    {
        "id": 5,
        "name": "Warehouse Echo",
        "location": "Phoenix, AZ",
        "shipping_cost_per_km": 2.2,
        "distance_to_customer_km": 350
    },
    {
        "id": 6,
        "name": "Warehouse Foxtrot",
        "location": "Philadelphia, PA",
        "shipping_cost_per_km": 1.7,
        "distance_to_customer_km": 100
    },
    {
        "id": 7,
        "name": "Warehouse Golf",
        "location": "San Antonio, TX",
        "shipping_cost_per_km": 1.9,
        "distance_to_customer_km": 500
    },
    {
        "id": 8,
        "name": "Warehouse Hotel",
        "location": "San Diego, CA",
        "shipping_cost_per_km": 2.1,
        "distance_to_customer_km": 275
    },
    {
        "id": 9,
        "name": "Warehouse India",
        "location": "Dallas, TX",
        "shipping_cost_per_km": 1.8,
        "distance_to_customer_km": 325
    },
    {
        "id": 10,
        "name": "Warehouse Juliet",
        "location": "San Jose, CA",
        "shipping_cost_per_km": 2.3,
        "distance_to_customer_km": 150
    }
]
'''

# Parse the JSON data
warehouses = json.loads(warehouses_json)

# Order quantity
order_quantity = 20

# Create a Custom Agent Class
class WarehouseAssistantAgent(AssistantAgent):
    def best_warehouse(self):
        prompt = f"""
            You are a Warehouse Assistant AI. Based on the given warehouse data and order quantity, calculate the total shipping cost for each warehouse and rank them in ascending order of cost. 

            Here is the warehouse data:
        {json.dumps(warehouses, indent=2)}

            Order quantity: {order_quantity}

            Your response should contain:
         only one list of warehouses with their total shipping cost which should be sorted by total shipping cost in ascending order.
         Please provide only the response dont need any code. Response should not need any steps, provies only the final output as list not json
        """
        return self.generate_reply(messages=[{"content": prompt, "role": "user"}])

llm_config = {"config_list": [
  {"model": "gpt-4o-mini", 
   "base_url": "https://oai-stock-search.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview", 
    "api_type": "azure",
    "api_key": "8S6mATWRVWLz5tux9nuCdhHmxOsverJ7YC4gEMohsOvsuVLkk2D4JQQJ99ALACYeBjFXJ3w3AAABACOGu8iG",
    "api_version": "2024-08-01-preview"}]
}
# Instantiate the Assistant Agent with a name and model configuration
assistant = WarehouseAssistantAgent(
    name="WarehouseAgent",
    llm_config=llm_config
)

async def query_assistant_agent():
    decision = await asyncio.to_thread(assistant.best_warehouse)
    print("Best Warehouse Decision:")
    print(decision)
asyncio.run(query_assistant_agent())
