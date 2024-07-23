import geocoder

# Get the current location based on IP address
g = geocoder.ip('me')

print(g)

# Extract latitude and longitude
latlng = g.latlng

# Print latitude and longitude
print(f"Latitude: {latlng[0]}, Longitude: {latlng[1]}")
