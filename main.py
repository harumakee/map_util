import sys
from geopy import Point
from geojson import Polygon, FeatureCollection
import json

from shape.circle import CircleZone
from flight_area.area import Area

if __name__ == "__main__":
    args = sys.argv

    if len(args) >= 2:
        if args[1] == "--help":
            print("usage")
        # TODO: ファイル出力を実装

    print("Define Flight Area")
    print("=============================")

    area_list: list[Polygon] = []
    while True:
        name = input("Name?: ")
        if name == "END":
            break
        elif name == "airport":
            print("<Airport>")

            point = Point(input("Airport Degit: "))
            area_list.append(CircleZone(9, point).get_polygon())
        else:
            print("<Area: " + name + ">")

            max_altitude = int(input("Altitude?: "))

            point_list: list[Point] = []
            while True:
                point = input("Insert Point: ")
                if point == "end":
                    break
                else:
                    point_list.append(Point(point))

            area_list.append(Area(name, point_list, max_altitude).make_area())

    # geojson_data = json.dump(FeatureCollection(area_list), None, indent=4)
    geojson_data = json.dumps(FeatureCollection(area_list), indent=4)
    print(geojson_data)
