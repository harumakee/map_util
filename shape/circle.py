from geopy import Point
from geojson import Polygon
import numpy
from geopy import distance
import re


class CircleZone:
    """円を表すクラス

    Attributes
    ----------
    radius : float
        半径[km]
    center : Point
        中心の座標（緯度経度）
    """

    def __init__(self, radius: float, center: Point) -> None:
        """円を定義する

        Parameters
        -----------
        radius : float
            半径[km]
        center : Point
            中心の座標（緯度経度）
        """
        self.radius = radius
        self.center = center

    def _calc_x_radius(self) -> float:
        """
        クラス属性の半径(km)から、地図の座標上での半径（経度用）を求める。
        """
        center_point: list[str] = self.center.format_decimal()
        outside_point = (
            distance.distance(kilometers=self.radius).destination(
                point=(self.center), bearing=90
            )
        ).format_decimal()

        center_coordinate: list[str] = center_point.replace(" ", "").split(",")
        outside_coordinate: list[str] = outside_point.replace(" ", "").split(",")

        return abs(float(outside_coordinate[1]) - float(center_coordinate[1]))

    def _calc_y_radius(self) -> float:
        """
        クラス属性の半径(km)から、地図の座標上での半径（緯度用）を求める。
        """
        center_point: list[str] = self.center.format_decimal()
        outside_point = (
            distance.distance(kilometers=self.radius).destination(
                point=(self.center), bearing=0
            )
        ).format_decimal()

        center_coordinate: list[str] = center_point.replace(" ", "").split(",")
        outside_coordinate: list[str] = outside_point.replace(" ", "").split(",")

        return abs(float(outside_coordinate[0]) - float(center_coordinate[0]))

    def get_polygon(self, precision: float = 0.01) -> Polygon:
        """
        円周上の点を計算し、Polygonデータを作成する。

        Parameter
        ----------
        precision : float
            点の間隔

        Returns
        ---------
        Geojson形式のPolygonデータ
        """
        theta = 0
        point_list = []
        while theta <= 2 * numpy.pi:
            x = self.center[1] + self._calc_x_radius() * numpy.cos(theta)
            y = self.center[0] + self._calc_y_radius() * numpy.sin(theta)
            point_list.append([x, y])
            theta += precision

        return Polygon(coordinates=[point_list])
