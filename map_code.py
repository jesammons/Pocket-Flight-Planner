import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import pandas as pd
from geopy.distance import geodesic

def get_airports():
    df = pd.read_excel('airports_data.xlsx')
    return df

def display_airports(df):
    airports_file = 'airports_list.txt'
    
    with open(airports_file, 'w') as file:
        file.write("List of Airports\n\n")
        
        for index, row in df.iterrows():
            file.write(f"{row['CITY']} --- {row['CODE']} --- {row['AIRPORT NAME']}\n\n")
    
    print(f"The list of airports has been saved to '{airports_file}'.")

def get_input(prompt, df):
    while True:
        user_input = input(prompt)
        user_input_upper = user_input.upper()

        matching_row = df[df['CODE'] == user_input_upper]

        if not matching_row.empty:
            print("Airport Code:", matching_row.iloc[0]['CODE'])
            print("Airport Name:", matching_row.iloc[0]['AIRPORT NAME'])

            lat, lon = matching_row.iloc[0]['LATITUDE'], matching_row.iloc[0]['LONGITUDE']

            #print("Latitude:", lat)
            #print("Longitude:", lon)

            return user_input_upper, lat, lon, matching_row.iloc[0]['AIRPORT NAME']
        else:
            print("Invalid airport code. Please enter a valid airport code.")


def get_city_input(prompt, df):
    while True:
        user_input = input(prompt)
        user_input_stripped = user_input.strip().upper()
        print("Stripped and uppercased user input:", user_input_stripped)
        print("Unique cities in the DataFrame:", df['CITY'].str.strip().str.upper().unique())

        matching_rows = df[df['CITY'].str.strip().str.upper() == user_input_stripped]

        if not matching_rows.empty:
            print(f"Airports in {user_input_stripped} city:")
            print(matching_rows[['AIRPORT NAME', 'CODE']])
            selected_airport = input("Enter the airport code you want to use: ")

            selected_airport_stripped = selected_airport.strip().upper()
            print("Stripped and uppercased selected airport code:", selected_airport_stripped)

           # Validate user input
            selected_airport_stripped = selected_airport.strip().upper()

            while selected_airport_stripped not in matching_rows['CODE'].str.strip().str.upper().values:
                print("Invalid input. Please choose a valid airport code.")
                selected_airport = input("Enter the airport code you want to use: ")
                selected_airport_stripped = selected_airport.strip().upper()

            selected_row = matching_rows[matching_rows['CODE'] == selected_airport.strip().upper()].iloc[0]

            return selected_row['CODE'], selected_row['LATITUDE'], selected_row['LONGITUDE'], selected_row['AIRPORT NAME']
        else:
            print("Invalid city. Please enter a valid city.")


def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).miles


def calculate_intermediate_points(departure_coordinates, arrival_coordinates, interval_miles=20):
    distance_miles = calculate_distance(departure_coordinates, arrival_coordinates)
    num_points = int(distance_miles / interval_miles) + 1

    lats, lons = [], []

    for i in range(num_points):
        fraction = i / (num_points - 1)
        intermediate_point = (
            departure_coordinates[0] + fraction * (arrival_coordinates[0] - departure_coordinates[0]),
            departure_coordinates[1] + fraction * (arrival_coordinates[1] - departure_coordinates[1])
        )
        lats.append(intermediate_point[0])
        lons.append(intermediate_point[1])

    return lats, lons


df = get_airports()

# Ask the user if they want to see the list of airports
user_choice = input("Would you like to see the list of airports? (yes/no): ").lower()
if user_choice == "yes":
    display_airports(df)

while True:
    user_choice = input("Do you want to input airport codes (A) or cities (C)? ").upper()

    if user_choice == "A":
        departing_ap, departing_lat, departing_lon, departing_name = get_input("Input your departing airport: ", df)
        arriving_ap, arriving_lat, arriving_lon, arriving_name = get_input("Input your arriving airport: ", df)
    elif user_choice == "C":
        departing_ap, departing_lat, departing_lon, departing_name = get_city_input("Input your departing city: ", df)
        arriving_ap, arriving_lat, arriving_lon, arriving_name = get_city_input("Input your arriving city: ", df)
    else:
        print("Invalid choice. Please enter either 'A' for airport codes or 'C' for cities.")
        continue

    if departing_ap != arriving_ap:
        break
    else:
        print("Departing and arriving airports cannot be the same. Please enter different airports.")

print("Departing airport:", departing_ap, "(", departing_name, ")")
print("Arriving airport:", arriving_ap, "(", arriving_name, ")")

departure_coordinates = (departing_lat, departing_lon)
arrival_coordinates = (arriving_lat, arriving_lon)
distance_miles = calculate_distance(departure_coordinates, arrival_coordinates)

average_cruising_speed = 547
flight_time_hours = distance_miles / average_cruising_speed

# After obtaining departure_coordinates and arrival_coordinates
intermediate_lats, intermediate_lons = calculate_intermediate_points(departure_coordinates, arrival_coordinates)

print("\nLatitude, Longitude:")
for lat, lon in zip(intermediate_lats, intermediate_lons):
    print(f"{lat:.6f}, {lon:.6f}")

print(f"\nDistance between {departing_ap} and {arriving_ap}: {distance_miles:.2f} miles")
print(f"Estimated flight time: {flight_time_hours:.2f} hours")

# Calculate bounding box for the departing and arriving airports
min_lon = min(departing_lon, arriving_lon) - 5
max_lon = max(departing_lon, arriving_lon) + 5
min_lat = min(departing_lat, arriving_lat) - 5
max_lat = max(departing_lat, arriving_lat) + 5

fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
ax.coastlines()
ax.add_feature(cartopy.feature.BORDERS, linestyle='-', linewidth=1)
ax.add_feature(cartopy.feature.STATES, linestyle='-', linewidth=1)

ax.add_feature(cartopy.feature.LAND, facecolor='darkseagreen', edgecolor='dimgray', linewidth=2)

# Add ocean in blue
ax.add_feature(cartopy.feature.OCEAN, facecolor='lightblue')

# plot a line between departing and arriving airports
ax.plot([departing_lon, arriving_lon], [departing_lat, arriving_lat], color='black', linewidth=3, transform=ccrs.PlateCarree())

# plot markers for departing and arriving airports in black color
ax.scatter(departing_lon, departing_lat, marker='o', color='royalblue', s=50, label=f'Departing: {departing_ap}', transform=ccrs.PlateCarree(), zorder =2)
ax.scatter(arriving_lon, arriving_lat, marker='o', color='firebrick', s=50, label=f'Arriving: {arriving_ap}', transform=ccrs.PlateCarree(), zorder =2)

# add legend for the markers at the bottom left
ax.legend(loc='lower left')

# add text for distance and time on the top right of the map
info_text = f"Distance: {distance_miles:.2f} miles\nEstimated Flight Time: {flight_time_hours:.2f} hours"
ax.text(0.95, 0.95, info_text, ha='right', va='top', transform=ax.transAxes, bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=0.5'))

ax.set_title(f"Flight Path from {departing_ap} to {arriving_ap}")

# Set the extent based on the bounding box
ax.set_extent([min_lon, max_lon, min_lat, max_lat])

file_path = "flight_map.png"
plt.savefig(file_path, format="png")