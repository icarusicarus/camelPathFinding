import folium
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def get_geojson_grid(upper_right, lower_left, n):

    all_boxes = []

    lat_steps = np.linspace(lower_left[0], upper_right[0], n+1)
    lon_steps = np.linspace(lower_left[1], upper_right[1], n+1)

    lat_stride = lat_steps[1] - lat_steps[0]
    lon_stride = lon_steps[1] - lon_steps[0]

    for lat in lat_steps[:-1]:
        for lon in lon_steps[:-1]:
            # Define dimensions of box in grid
            upper_left = [lon, lat + lat_stride]
            upper_right = [lon + lon_stride, lat + lat_stride]
            lower_right = [lon + lon_stride, lat]
            lower_left = [lon, lat]

            # Define json coordinates for polygon
            coordinates = [
                upper_left,
                upper_right,
                lower_right,
                lower_left,
                upper_left
            ]

            geo_json = {"type": "FeatureCollection",
                        "properties":{
                            "lower_left": lower_left,
                            "upper_right": upper_right
                        },
                        "features":[]}

            grid_feature = {
                "type":"Feature",
                "geometry":{
                    "type":"Polygon",
                    "coordinates": [coordinates],
                }
            }

            geo_json["features"].append(grid_feature)

            all_boxes.append(geo_json)

    return all_boxes


lower_left = [35.230602, 129.080897]
upper_right = [35.233336, 129.084722]

grid = get_geojson_grid(upper_right, lower_left, 60)

m = folium.Map(location=(35.2320726,129.0833546), zoom_start=18)
folium.Marker(
    location=[35.233269, 129.082843],
    popup="특공관", icon=folium.Icon(color="red",icon="star")).add_to(m)
folium.Marker(
    location=[35.232635, 129.082850],
    popup="본부", icon=folium.Icon(color="red",icon="star")).add_to(m)
folium.Marker(
    location=[35.230957, 129.082474],
    popup="제도관", icon=folium.Icon(color="red",icon="star")).add_to(m)
for i, geo_json in enumerate(grid):

    color = plt.cm.Reds(i / len(grid))
    color = mpl.colors.to_hex(color)

    gj = folium.GeoJson(geo_json,
                        style_function=lambda feature, #color=color
                                                    : {
                                                                        #'fillColor': color,
                                                                        'color':"blue",
                                                                        'weight': 1,
                                                                        #'dashArray': '5, 5',
                                                                        'fillOpacity': 0,
                                                                    })
    popup = folium.Popup("example popup {}".format(i))
    gj.add_child(popup)

    m.add_child(gj)
m.save('camelMap.html')