# import openai
# import pandas as pd
# from geopy.geocoders import Nominatim
# from geopy.distance import geodesic
# import requests

# # Set OpenAI API key (ensure you have your OpenAI API key from Azure)
# openai.api_key = "5c87LpTdEoFIwrlPVvpSvQWw44lhivTrVQdSYYqEdz53qLpvTXuEJQQJ99AKAC77bzfXJ3w3AAABACOGq8qs"

# # Load the Excel file and sheets
# file_path = 'stock-sample 1.xlsx'
# inventory_df = pd.read_excel(file_path, sheet_name='inventory')
# warehouse_df = pd.read_excel(file_path, sheet_name='warehouse')

# # Assume order details
# order_location = 'Nashville, TN'  # Order location
# order_sku = "ELE-IPH14-001"  # SKU of the order
# order_quantity = 20  # Order quantity

# # Initialize geolocator
# geolocator = Nominatim(user_agent="warehouse_locator")

# # Function to calculate distance between two locations (using geopy)
# def get_distance(location1, location2):
#     # Get the coordinates for both locations
#     loc1 = geolocator.geocode(location1)
#     loc2 = geolocator.geocode(location2)
    
#     if loc1 and loc2:
#         # Use geopy's geodesic method to calculate the distance between two (lat, lon) pairs
#         coords_1 = (loc1.latitude, loc1.longitude)
#         coords_2 = (loc2.latitude, loc2.longitude)
        
#         # Calculate and return the distance in kilometers
#         return geodesic(coords_1, coords_2).km
#     else:
#         return None

# # Function to calculate shipping cost based on distance and charge per unit per km
# def calculate_shipping_cost(distance_km, charge_per_unit_km, quantity):
#     return distance_km * charge_per_unit_km * quantity

# # Define a prompt for OpenAI to decide the best warehouse
# def choose_best_warehouse(distance, shipping_costs):
#     prompt = f"""
#     You are a shipping logistics expert. You are given the following factors for choosing the best warehouse for an order:
#     - Distance to warehouse: {distance} km
#     - Shipping costs per unit per km for each warehouse: {shipping_costs}
    
#     Your task is to analyze these factors and decide which warehouse offers the lowest shipping cost.
    
#     Please choose the best warehouse based on the lowest shipping cost and provide the name of the warehouse.
#     """
    
#     response = openai.Completion.create(
#         model="gpt-4o",  # Use the model available in your Azure OpenAI subscription
#         prompt=prompt,
#         max_tokens=150,
#         temperature=0.7
#     )
    
#     return response.choices[0].text.strip()

# # Initialize variables to track best warehouse
# best_warehouse = None
# lowest_shipping_cost = float('inf')

# # Iterate over warehouse locations to calculate shipping cost
# for index, row in warehouse_df.iterrows():
#     warehouse_location = row['Location']
#     shipping_charge_per_unit_km = row['Shipping Charge/unit/Km']
    
#     # Step 1: Calculate distance
#     distance_km = get_distance(order_location, warehouse_location)
    
#     if distance_km is not None:
#         # Step 2: Calculate the total shipping cost for this warehouse
#         shipping_cost = calculate_shipping_cost(distance_km, shipping_charge_per_unit_km, order_quantity)
        
#         # Step 3: Send the data to OpenAI to decide the best warehouse
#         shipping_costs = {
#             warehouse_location: shipping_cost
#         }
#         decision = choose_best_warehouse(distance_km, shipping_costs)
        
#         if decision.lower() == warehouse_location.lower():
#             if shipping_cost < lowest_shipping_cost:
#                 lowest_shipping_cost = shipping_cost
#                 best_warehouse = warehouse_location

# # Output the best warehouse and the corresponding shipping cost
# if best_warehouse:
#     print(f"Best Warehouse for Order SKU {order_sku}: {best_warehouse}")
#     print(f"Shipping Cost: ${lowest_shipping_cost:.2f}")
# else:
#     print("No warehouse found with a valid location.")

import openai
import pandas as pd
import os
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic  # Import geodesic to calculate the distance

# Azure OpenAI Setup (API key and endpoint from your Azure OpenAI resource)
azure_api_key = "58FOhI1po5XI4Puuoo6oOLHlOoFEbWoJQ9vWx67eixvD7pdE6DXZJQQJ99ALACYeBjFXJ3w3AAABACOGVIPg"
azure_endpoint = "https://stockagentopenai.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2024-08-01-preview"

# Set OpenAI API key (ensure you have your OpenAI API key from Azure)
openai.api_key = azure_api_key
openai.base_url = azure_endpoint
openai.api_version = "2024-08-01-preview"

# Load the Excel file and sheets
file_path = 'stock-sample 1.xlsx'
inventory_df = pd.read_excel(file_path, sheet_name='inventory')
warehouse_df = pd.read_excel(file_path, sheet_name='warehouse')

# Assume order details
order_location = 'Nashville, TN'  # Order location
order_sku = "ELE-IPH14-001"  # SKU of the order
order_quantity = 20  # Order quantity

# Initialize geolocator
geolocator = Nominatim(user_agent="warehouse_locator")

# Function to calculate distance between two locations (using geopy)
def get_distance(location1, location2):
    # Get the coordinates for both locations
    loc1 = geolocator.geocode(location1)
    loc2 = geolocator.geocode(location2)
    
    if loc1 and loc2:
        # Use geopy's geodesic method to calculate the distance between two (lat, lon) pairs
        coords_1 = (loc1.latitude, loc1.longitude)
        coords_2 = (loc2.latitude, loc2.longitude)
        
        # Calculate and return the distance in kilometers
        return geodesic(coords_1, coords_2).km
    else:
        return None

# Function to calculate shipping cost based on distance and charge per unit per km
def calculate_shipping_cost(distance_km, charge_per_unit_km, quantity):
    return distance_km * charge_per_unit_km * quantity

# Define a prompt for OpenAI to decide the best warehouse
def choose_best_warehouse(distance, shipping_costs):
    # Creating the conversation-style input expected by chat models like GPT-3.5/4
    messages = [
        {"role": "system", "content": "You are a shipping logistics expert."},
        {"role": "user", "content": f"""
        I have the following shipping cost data for warehouses:
        - Distance to warehouse: {distance} km
        - Shipping costs per unit per km for each warehouse: {shipping_costs}
        
        Based on this, please determine which warehouse offers the lowest shipping cost.
        """}
    ]

    response = openai.chat.completions.create(
        model="gpt-4",  # or another model like 'gpt-3.5-turbo'
        messages=messages,
        max_tokens=150
    )

    
    # response = openai.chat.completions.create(
    #     model="gpt-4o",  # You can also use "gpt-3.5-turbo" if needed
    #     messages=messages,
    #     max_tokens=150,
    #     temperature=0.7
    # )
    
    # Extract the assistant's response
    return response['choices'][0]['message']['content'].strip()

# Initialize variables to track best warehouse
best_warehouse = None
lowest_shipping_cost = float('inf')

# Iterate over warehouse locations to calculate shipping cost
for index, row in warehouse_df.iterrows():
    warehouse_location = row['Location']
    shipping_charge_per_unit_km = row['Shipping Charge/unit/Km']
    
    # Step 1: Calculate distance
    distance_km = get_distance(order_location, warehouse_location)
    
    if distance_km is not None:
        # Step 2: Calculate the total shipping cost for this warehouse
        shipping_cost = calculate_shipping_cost(distance_km, shipping_charge_per_unit_km, order_quantity)
        
        # Step 3: Send the data to OpenAI to decide the best warehouse
        shipping_costs = {
            warehouse_location: shipping_cost
        }
        decision = choose_best_warehouse(distance_km, shipping_costs)
        
        if decision.lower() == warehouse_location.lower():
            if shipping_cost < lowest_shipping_cost:
                lowest_shipping_cost = shipping_cost
                best_warehouse = warehouse_location

# Output the best warehouse and the corresponding shipping cost
if best_warehouse:
    print(f"Best Warehouse for Order SKU {order_sku}: {best_warehouse}")
    print(f"Shipping Cost: ${lowest_shipping_cost:.2f}")
else:
    print("No warehouse found with a valid location.")
