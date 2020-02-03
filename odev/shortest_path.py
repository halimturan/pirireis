import pyvisgraph as vg
import folium

polys = [[vg.Point(6.0, 7.0), vg.Point(20.0, 7.0), vg.Point(20.0, 14.0), vg.Point(6.0, 14.0)],
         [vg.Point(5.0, 17.0), vg.Point(8.0, 17.0), vg.Point(8.0, 20.0), vg.Point(5.0, 20.0)]]
g = vg.VisGraph()
g.build(polys)

target_list = [{"target_name": "hedef_x", "coordinates": [5.0, 2.0]},
               {"target_name": "hedef_y", "coordinates": [17.0, 1.5]},
               {"target_name": "hedef_z", "coordinates": [9.0, 22.0]},
               {"target_name": "hedef_t", "coordinates": [1.0, 3.0]}]
target_list.insert(0, {"target_name": "start", "coordinates": [0.0, 0.0]})
target_list.append({"target_name": "return", "coordinates": [0.0, 0.0]})

geomap = folium.Map([0, 0], zoom_start=5)
geopath_polygon = []
for arr in polys:
    geopath_polygon.append([[coord.x, coord.y] for coord in arr])

polypath = polys
for i in geopath_polygon:
    folium.Polygon(i, fill=True, color='red').add_to(geomap)

file = open("output.txt", "w")
file.write("[")
for i in range(len(target_list)):
    if i != len(target_list) - 1:
        shortest_path = g.shortest_path(vg.Point(target_list[i]["coordinates"][0], target_list[i]["coordinates"][1]),
                                        vg.Point(target_list[i + 1]["coordinates"][0], target_list[i + 1]["coordinates"][1]))
        geopath = [[point.x, point.y] for point in shortest_path]
        file.write(f'({target_list[i+1]["target_name"]}, {geopath}),\n')
        print(geopath)
        for point in geopath:
            folium.Marker(point, popup=str(point)).add_to(geomap)
            folium.PolyLine(geopath).add_to(geomap)
            folium.Marker(geopath[0], icon=folium.Icon(color='red')).add_to(geomap)
            folium.Marker(geopath[-1], icon=folium.Icon(color='red')).add_to(geomap)
file.write("]")
file.close()
output_name = 'demo.html'
geomap.save(output_name)
