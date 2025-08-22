import os
import json
from typing import Any, Dict, List, Optional
from flask import Flask, jsonify, request
from flask_cors import CORS

DATA_DIR = os.getenv("DATA_DIR", os.path.join(os.getcwd(), "data"))
BOUNDARY_PATH = os.path.join(DATA_DIR, "campus_boundary.geojson")
BUILDINGS_PATH = os.path.join(DATA_DIR, "buildings.geojson")
NAV_CONFIG_PATH = os.path.join(DATA_DIR, "navigation_config.json")




def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Enable CORS for all routes (adjust origins for production as needed)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route("/", methods=["GET"])
    def root():
        return jsonify({"status": "Backend is running", "message": "Welcome to Campus Connect!"}), 200


    @app.route("/api/events", methods=["GET"])
    def get_events():
        events = [
            {
                "id": "1",
                "title": "Robotics Workshop",
                "organizer": "Tech Club",
                "location": "Room 204",
                "time": "2025-08-22T14:00:00Z",
                "description": "Hands-on robotics session."
            },
            {
                "id": "2",
                "title": "Cultural Night",
                "organizer": "Cultural Committee",
                "location": "Auditorium",
                "time": "2025-08-23T19:00:00Z",
                "description": "Music, dance, and more."
            },
            {
                "id": "3",
                "title": "Placement Talk",
                "organizer": "T&P Cell",
                "location": "Seminar Hall",
                "time": "2025-08-24T10:00:00Z",
                "description": "Resume and interview tips."
            }
        ]
        return jsonify(events), 200



    @app.route("/api/campus/boundary", methods=["GET"])
    def get_campus_boundary():
        boundary = _load_campus_boundary()
        if boundary is None:
            return jsonify({"id": "campus", "name": "Campus (placeholder)", "coordinates": []}), 200
        return jsonify(boundary), 200

    @app.route("/api/locations", methods=["GET"])
    def get_locations():
        locations = _load_locations()
        return jsonify(locations), 200

    @app.route("/api/locations/<loc_id>", methods=["GET"])
    def get_location_by_id(loc_id: str):
        for loc in _load_locations():
            if str(loc.get("id")) == str(loc_id):
                return jsonify(loc), 200
        return jsonify({"error": "Location not found"}), 404



    @app.route("/api/navigation/config", methods=["GET"])
    def get_navigation_config():
        cfg = _load_nav_config()
        return jsonify(cfg), 200



    @app.route("/api/navigation/all", methods=["GET"])
    def get_navigation_all():
        boundary = _load_campus_boundary()
        if boundary is None:
            boundary = {"id": "campus", "name": "Campus (placeholder)", "coordinates": []}
        locations = _load_locations()
        cfg = _load_nav_config()
        return jsonify({
            "config": cfg,
            "boundary": boundary,
            "locations": locations,
        }), 200


    # -----------------------------
    # Helpers: data loading & convert
    # -----------------------------

    def _safe_read_json(path: str) -> Optional[Dict[str, Any]]:
        try:
            if not os.path.isfile(path):
                return None
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Failed to read JSON from {path}: {e}", flush=True)
            return None

    def _geojson_outer_ring_to_latlng(geom: Dict[str, Any]) -> List[List[float]]:
        if not geom or "type" not in geom or "coordinates" not in geom:
            return []

        gtype = geom["type"]
        coords = geom["coordinates"]

        ring: List[List[float]] = []

        if gtype == "Polygon":
            if not coords or not coords[0]:
                return []
            outer = coords[0]
            ring = [[pt[1], pt[0]] for pt in outer if isinstance(pt, (list, tuple)) and len(pt) >= 2]
        elif gtype == "MultiPolygon":
            if not coords:
                return []
            candidate = max(coords, key=lambda poly: len(poly[0]) if poly and poly[0] else 0)
            if not candidate or not candidate[0]:
                return []
            outer = candidate[0]
            ring = [[pt[1], pt[0]] for pt in outer if isinstance(pt, (list, tuple)) and len(pt) >= 2]
        else:
            return []

        if ring and ring[0] != ring[-1]:
            ring.append(ring[0])
        return ring

    def _load_campus_boundary() -> Optional[Dict[str, Any]]:
        data = _safe_read_json(BOUNDARY_PATH)
        if not data:
            return None

        if data.get("type") == "Feature":
            geom = data.get("geometry", {})
            name = data.get("properties", {}).get("name") or "Campus"
        elif data.get("type") in ("Polygon", "MultiPolygon"):
            geom = data
            name = "Campus"
        else:
            if data.get("type") == "FeatureCollection" and data.get("features"):
                feat = data["features"][0]
                geom = feat.get("geometry", {})
                name = feat.get("properties", {}).get("name") or "Campus"
            else:
                return None

        coords_latlng = _geojson_outer_ring_to_latlng(geom)
        return {"id": "campus", "name": name, "coordinates": coords_latlng}

    def _load_locations() -> List[Dict[str, Any]]:
        data = _safe_read_json(BUILDINGS_PATH)
        if not data:
            return [
                {
                    "id": "b1",
                    "name": "Main Block",
                    "category": "Academic",
                    "coordinates": [[16.4945, 80.5123], [16.4946, 80.5129], [16.4941, 80.5130], [16.4940, 80.5124], [16.4945, 80.5123]],
                    "description": "Central academic building.",
                    "imageUrl": "https://example.com/main-block.jpg",
                },
                {
                    "id": "b2",
                    "name": "Auditorium",
                    "category": "Facility",
                    "coordinates": [[16.4930, 80.5110], [16.4934, 80.5115], [16.4929, 80.5118], [16.4926, 80.5112], [16.4930, 80.5110]],
                    "description": "Events and cultural programs.",
                    "imageUrl": "https://example.com/auditorium.jpg",
                },
            ]

        feats: List[Dict[str, Any]] = []
        if data.get("type") == "FeatureCollection":
            for feat in data.get("features", []):
                geom = feat.get("geometry", {})
                props = feat.get("properties", {})
                ring = _geojson_outer_ring_to_latlng(geom)
                if not ring:
                    continue
                feats.append({
                    "id": str(props.get("id") or props.get("code") or props.get("name") or len(feats) + 1),
                    "name": str(props.get("name") or "Building"),
                    "category": str(props.get("category") or "General"),
                    "coordinates": ring,
                    "description": str(props.get("description") or ""),
                    "imageUrl": str(props.get("imageUrl") or ""),
                })
        elif data.get("type") == "Feature":
            geom = data.get("geometry", {})
            props = data.get("properties", {})
            ring = _geojson_outer_ring_to_latlng(geom)
            if ring:
                feats.append({
                    "id": str(props.get("id") or props.get("code") or props.get("name") or 1),
                    "name": str(props.get("name") or "Building"),
                    "category": str(props.get("category") or "General"),
                    "coordinates": ring,
                    "description": str(props.get("description") or ""),
                    "imageUrl": str(props.get("imageUrl") or ""),
                })
        return feats

    def _load_nav_config() -> Dict[str, Any]:
        data = _safe_read_json(NAV_CONFIG_PATH)
        default = {
            "center": [16.493, 80.513],
            "defaultZoom": 17,
            "categoryColors": {
                "Academic": "#2563eb",
                "Admin": "#f59e0b",
                "Hostel": "#10b981",
                "Facility": "#8b5cf6",
                "Sports": "#ef4444",
                "General": "#3b82f6",
            },
        }
        if isinstance(data, dict):
            cfg = default.copy()
            for k in ("center", "defaultZoom", "categoryColors"):
                if k in data:
                    cfg[k] = data[k]
            return cfg
        return default



    @app.route("/api/events", methods=["POST"])
    def create_event():
        payload = request.get_json(silent=True) or {}
        print("[POST /api/events] Received payload:", payload, flush=True)
        return jsonify({"message": "Event created successfully"}), 201

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    # Bind to 0.0.0.0 for container/VM compatibility
    app.run(host="0.0.0.0", port=port, debug=debug)

