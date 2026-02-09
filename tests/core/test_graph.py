"""
Tests for core.graph module.
"""

import pytest
from core.graph import Node, Edge, GraphManager


class TestNode:
    """Tests for Node class."""

    def test_node_creation(self):
        """Test basic node creation."""
        node = Node.create(name="pump", x=100.0, y=200.0)
        assert node.name == "pump"
        assert node.x == 100.0
        assert node.y == 200.0
        assert node.id is not None
        assert len(node.id) > 0

    def test_node_with_custom_id(self):
        """Test node with custom ID."""
        node = Node.create(name="reactor", x=50.0, y=60.0, id="reactor_1")
        assert node.id == "reactor_1"

    def test_node_with_properties(self):
        """Test node with custom properties."""
        node = Node.create(name="pump", x=0, y=0, capacity=100, efficiency=0.85)
        assert node.properties["capacity"] == 100
        assert node.properties["efficiency"] == 0.85

    def test_node_serialization(self):
        """Test node serialization and deserialization."""
        node = Node.create(name="pump", x=100, y=200, id="pump_1", capacity=50)
        data = node.to_dict()

        restored = Node.from_dict(data)
        assert restored.id == node.id
        assert restored.name == node.name
        assert restored.x == node.x
        assert restored.y == node.y
        assert restored.properties == node.properties


class TestEdge:
    """Tests for Edge class."""

    def test_edge_creation(self):
        """Test basic edge creation."""
        edge = Edge.create(source="pump_1", target="reactor_1", type="material")
        assert edge.source == "pump_1"
        assert edge.target == "reactor_1"
        assert edge.type == "material"
        assert edge.id is not None

    def test_edge_with_properties(self):
        """Test edge with custom properties."""
        edge = Edge.create(
            source="pump_1",
            target="reactor_1",
            type="energy",
            flow_rate=100.0,
            temperature=25.0
        )
        assert edge.properties["flow_rate"] == 100.0
        assert edge.properties["temperature"] == 25.0

    def test_edge_serialization(self):
        """Test edge serialization and deserialization."""
        edge = Edge.create(
            source="node_1",
            target="node_2",
            type="stream",
            id="edge_1",
            flow=50
        )
        data = edge.to_dict()

        restored = Edge.from_dict(data)
        assert restored.id == edge.id
        assert restored.source == edge.source
        assert restored.target == edge.target
        assert restored.type == edge.type
        assert restored.properties == edge.properties


class TestGraphManager:
    """Tests for GraphManager class."""

    def test_create_node(self):
        """Test creating a node."""
        graph = GraphManager()
        node = graph.create_node(type="pump", x=100, y=200)

        assert node is not None
        assert graph.get_node(node.id) == node

    def test_delete_node(self):
        """Test deleting a node."""
        graph = GraphManager()
        node = graph.create_node(type="pump", x=100, y=200)
        node_id = node.id

        assert graph.delete_node(node_id)
        assert graph.get_node(node_id) is None

    def test_move_node(self):
        """Test moving a node."""
        graph = GraphManager()
        node = graph.create_node(type="pump", x=100, y=200)

        moved_node = graph.move_node(node.id, x=300, y=400)
        assert moved_node.x == 300
        assert moved_node.y == 400

    def test_create_edge(self):
        """Test creating an edge."""
        graph = GraphManager()
        node1 = graph.create_node(type="pump", x=0, y=0)
        node2 = graph.create_node(type="reactor", x=100, y=100)

        edge = graph.create_edge(
            source=node1.id,
            target=node2.id,
            type="material"
        )

        assert edge is not None
        assert graph.get_edge(edge.id) == edge

    def test_create_edge_invalid_nodes(self):
        """Test creating an edge with invalid nodes."""
        graph = GraphManager()
        edge = graph.create_edge(
            source="nonexistent_1",
            target="nonexistent_2",
            type="material"
        )
        assert edge is None

    def test_delete_edge(self):
        """Test deleting an edge."""
        graph = GraphManager()
        node1 = graph.create_node(type="pump", x=0, y=0)
        node2 = graph.create_node(type="reactor", x=100, y=100)
        edge = graph.create_edge(source=node1.id, target=node2.id, type="material")
        edge_id = edge.id

        assert graph.delete_edge(edge_id)
        assert graph.get_edge(edge_id) is None

    def test_delete_node_deletes_connected_edges(self):
        """Test that deleting a node removes all connected edges."""
        graph = GraphManager()
        node1 = graph.create_node(type="pump", x=0, y=0)
        node2 = graph.create_node(type="reactor", x=100, y=100)
        node3 = graph.create_node(type="separator", x=200, y=200)

        edge1 = graph.create_edge(source=node1.id, target=node2.id, type="material")
        edge2 = graph.create_edge(source=node2.id, target=node3.id, type="material")

        graph.delete_node(node2.id)

        assert graph.get_edge(edge1.id) is None
        assert graph.get_edge(edge2.id) is None

    def test_get_edges_from_node(self):
        """Test getting outgoing edges from a node."""
        graph = GraphManager()
        node1 = graph.create_node(type="pump", x=0, y=0)
        node2 = graph.create_node(type="reactor", x=100, y=100)
        node3 = graph.create_node(type="separator", x=200, y=200)

        edge1 = graph.create_edge(source=node1.id, target=node2.id, type="material")
        edge2 = graph.create_edge(source=node1.id, target=node3.id, type="energy")

        outgoing = graph.get_edges_from_node(node1.id)
        assert len(outgoing) == 2
        assert edge1 in outgoing
        assert edge2 in outgoing

    def test_get_edges_to_node(self):
        """Test getting incoming edges to a node."""
        graph = GraphManager()
        node1 = graph.create_node(type="pump", x=0, y=0)
        node2 = graph.create_node(type="reactor", x=100, y=100)
        node3 = graph.create_node(type="pump", x=200, y=200)

        edge1 = graph.create_edge(source=node1.id, target=node2.id, type="material")
        edge2 = graph.create_edge(source=node3.id, target=node2.id, type="material")

        incoming = graph.get_edges_to_node(node2.id)
        assert len(incoming) == 2
        assert edge1 in incoming
        assert edge2 in incoming

    def test_serialization(self):
        """Test graph serialization and deserialization."""
        graph1 = GraphManager()
        node1 = graph1.create_node(type="pump", x=100, y=200, id="pump_1")
        node2 = graph1.create_node(type="reactor", x=300, y=400, id="reactor_1")
        edge = graph1.create_edge(source=node1.id, target=node2.id, type="material")

        data = graph1.to_dict()

        graph2 = GraphManager()
        graph2.from_dict(data)

        assert graph2.get_node("pump_1") is not None
        assert graph2.get_node("reactor_1") is not None
        assert len(graph2.edges) == 1

    def test_node_property(self):
        """Test setting node properties."""
        graph = GraphManager()
        node = graph.create_node(type="pump", x=0, y=0)

        graph.set_node_property(node.id, "capacity", 100)

        updated_node = graph.get_node(node.id)
        assert updated_node.properties["capacity"] == 100

    def test_edge_property(self):
        """Test setting edge properties."""
        graph = GraphManager()
        node1 = graph.create_node(type="pump", x=0, y=0)
        node2 = graph.create_node(type="reactor", x=100, y=100)
        edge = graph.create_edge(source=node1.id, target=node2.id, type="material")

        graph.set_edge_property(edge.id, "flow_rate", 50.0)

        updated_edge = graph.get_edge(edge.id)
        assert updated_edge.properties["flow_rate"] == 50.0

    def test_headless_callbacks(self):
        """Test callbacks work without QApplication."""
        graph = GraphManager()

        created_nodes = []
        graph.on_node_created(lambda n: created_nodes.append(n))

        node = graph.create_node(type="pump", x=0, y=0)

        assert len(created_nodes) == 1
        assert created_nodes[0] == node
