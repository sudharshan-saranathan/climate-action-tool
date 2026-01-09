# Encoding: utf-8
# Module name: scene
# Description: A QGraphicsScene for rendering GeoJSON maps

# Imports (standard)
from __future__ import annotations
import os
import json

# Imports (third party)
import geopandas
from PySide6 import QtCore, QtWidgets

# Imports (local):
from gui.maps.outline import Outline


# Class Scene:
class Scene(QtWidgets.QGraphicsScene):
    """A QGraphicsScene for rendering GeoJSON map data."""

    # Initializer:
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)

        # Attribute(s):
        self.geo_data = None
        self.geo_rect = QtCore.QRectF()
        self.geo_zoom = 250.0

        # Store map items:
        self._states: list[Outline] = []

        # Load the default map (India):
        self._load_default_map()

    # Load the default map:
    def _load_default_map(self):
        """Load the default India map from assets."""

        # Path to the geojson file:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        map_path = os.path.join(base_path, "assets", "maps", "india-state.geojson")

        if os.path.exists(map_path):
            with open(map_path, "r", encoding="utf-8") as f:
                obj = json.load(f)
                data = geopandas.GeoDataFrame.from_features(obj.get("features", []))
                self.render_geojson(data)

    # Convert scene-coordinates to lat/lon:
    def scene_to_geo(self, pos: QtCore.QPointF) -> tuple[float, float]:
        """Convert scene coordinates to geographic coordinates (longitude, latitude)."""
        minx, miny, maxx, maxy = self.geo_rect
        lon = (pos.x() / self.geo_zoom) + minx
        lat = maxy - (pos.y() / self.geo_zoom)
        return lon, lat

    # Convert lat/lon to scene-coordinates:
    def geo_to_scene(self, lon: float, lat: float) -> QtCore.QPointF:
        """Convert geographic coordinates (longitude, latitude) to scene coordinates."""
        minx, miny, maxx, maxy = self.geo_rect
        x = (lon - minx) * self.geo_zoom
        y = (maxy - lat) * self.geo_zoom
        return QtCore.QPointF(x, y)

    # Render GeoJSON data onto the scene:
    def render_geojson(self, geo_data: geopandas.GeoDataFrame) -> None:
        """Draw the provided GeoJSON data onto the scene using QGraphicsPathItem."""

        # Store the geo data:
        self.geo_data = geo_data
        self.geo_rect = self.geo_data.total_bounds

        minx, miny, maxx, maxy = self.geo_rect
        delta_x = maxx - minx if (maxx - minx) != 0 else 1
        delta_y = maxy - miny if (maxy - miny) != 0 else 1
        width = delta_x * self.geo_zoom
        height = delta_y * self.geo_zoom

        self.setSceneRect(QtCore.QRectF(0, 0, width, height))
        self.clear_map()

        # Render individual polygon geometries:
        for _, row in self.geo_data.iterrows():
            geom = getattr(row, "geometry", None)
            if geom is None:
                continue

            state = str(row["st_nm"]) if "st_nm" in row else ""
            gtype = getattr(geom, "geom_type", "")

            if gtype == "Polygon":
                polygons = [geom]
            elif gtype == "MultiPolygon":
                polygons = [
                    polygon
                    for polygon in getattr(geom, "geoms", [])
                    if getattr(polygon, "geom_type", "") == "Polygon"
                ]
            else:
                polygons = []

            for poly in polygons:
                region = Outline(poly, minx, maxy, zoom=self.geo_zoom)
                region.setObjectName(state)
                self.addItem(region)
                self._states.append(region)

    # Clear all map items:
    def clear_map(self):
        """Clear all map items from the scene."""
        for state in self._states:
            self.removeItem(state)
        self._states.clear()

    # Load a GeoJSON file:
    def load_geojson(self, file_path: str) -> None:
        """Load and render a GeoJSON file."""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                obj = json.load(f)
                data = geopandas.GeoDataFrame.from_features(obj.get("features", []))
                self.render_geojson(data)
