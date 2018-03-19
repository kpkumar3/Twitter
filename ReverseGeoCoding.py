
# coding: utf-8

#Sample code to reverse geo map. 
#Next steps: Convert this into a function, pass latitude and longitude and return the location details.
from geopy.geocoders import GoogleV3
geolocator = GoogleV3()
location = geolocator.reverse("27.91, -82.35")
print(location[0])

