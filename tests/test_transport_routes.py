"""
Tests for the transport routes module.
"""
import pytest
from src.transport_routes import TransportRouteSystem, Stop

class TestTransportRouteSystem:
    def setup_method(self):
        """Set up test fixtures"""
        self.system = TransportRouteSystem()
        self.route1 = "route1"
        self.route2 = "route2"
        self.stop1 = Stop("stop1", "First Stop")
        self.stop2 = Stop("stop2", "Second Stop")
        self.stop3 = Stop("stop3", "Third Stop")

    def test_add_route_basic(self):
        """Test basic route addition"""
        self.system.add_route(self.route1)
        assert self.route1 in self.system.routes
        assert len(self.system.routes[self.route1]) == 0

    def test_add_route_validation(self):
        """Test route addition validation"""
        # Test empty route ID
        with pytest.raises(ValueError, match="Route ID cannot be empty"):
            self.system.add_route("")

        # Test duplicate route
        self.system.add_route(self.route1)
        with pytest.raises(ValueError, match="already exists"):
            self.system.add_route(self.route1)

    def test_add_stop_to_route_basic(self):
        """Test basic stop addition to route"""
        self.system.add_route(self.route1)
        self.system.add_stop_to_route(self.route1, self.stop1)
        
        assert self.stop1 in self.system.routes[self.route1]
        assert self.route1 in self.system.stop_to_routes[self.stop1.id]

    def test_add_stop_to_route_validation(self):
        """Test stop addition validation"""
        # Test non-existent route
        with pytest.raises(ValueError, match="does not exist"):
            self.system.add_stop_to_route("nonexistent", self.stop1)

        # Test invalid stop
        self.system.add_route(self.route1)
        with pytest.raises(ValueError, match="required"):
            self.system.add_stop_to_route(self.route1, None)

        # Test duplicate stop (should not raise error)
        self.system.add_stop_to_route(self.route1, self.stop1)
        self.system.add_stop_to_route(self.route1, self.stop1)
        assert len(self.system.routes[self.route1]) == 1

    def test_remove_stop_from_route_basic(self):
        """Test basic stop removal from route"""
        self.system.add_route(self.route1)
        self.system.add_stop_to_route(self.route1, self.stop1)
        self.system.remove_stop_from_route(self.route1, self.stop1.id)
        
        assert self.stop1 not in self.system.routes[self.route1]
        assert self.stop1.id not in self.system.stop_to_routes

    def test_remove_stop_from_route_validation(self):
        """Test stop removal validation"""
        self.system.add_route(self.route1)
        
        # Test non-existent route
        with pytest.raises(ValueError, match="does not exist"):
            self.system.remove_stop_from_route("nonexistent", self.stop1.id)

        # Test non-existent stop
        with pytest.raises(ValueError, match="not found in route"):
            self.system.remove_stop_from_route(self.route1, "nonexistent")

    def test_get_routes_by_stop_basic(self):
        """Test basic route retrieval by stop"""
        # Setup multiple routes with common stops
        self.system.add_route(self.route1)
        self.system.add_route(self.route2)
        
        self.system.add_stop_to_route(self.route1, self.stop1)
        self.system.add_stop_to_route(self.route2, self.stop1)
        
        routes = self.system.get_routes_by_stop(self.stop1.id)
        assert len(routes) == 2
        assert self.route1 in routes
        assert self.route2 in routes

    def test_get_routes_by_stop_validation(self):
        """Test route retrieval validation"""
        # Test empty stop ID
        with pytest.raises(ValueError, match="Stop ID cannot be empty"):
            self.system.get_routes_by_stop("")

        # Test non-existent stop (should return empty set)
        routes = self.system.get_routes_by_stop("nonexistent")
        assert len(routes) == 0

    def test_get_stops_in_route_basic(self):
        """Test basic stop retrieval for route"""
        self.system.add_route(self.route1)
        self.system.add_stop_to_route(self.route1, self.stop1)
        self.system.add_stop_to_route(self.route1, self.stop2)
        
        stops = self.system.get_stops_in_route(self.route1)
        assert len(stops) == 2
        assert self.stop1 in stops
        assert self.stop2 in stops

    def test_get_stops_in_route_validation(self):
        """Test stop retrieval validation"""
        with pytest.raises(ValueError, match="Route ID cannot be empty"):
            self.system.get_stops_in_route("")
            
        with pytest.raises(ValueError, match="does not exist"):
            self.system.get_stops_in_route("nonexistent")

    def test_complex_route_network(self):
        """Test a more complex route network scenario"""
        # Create a network of routes and stops
        routes = [self.route1, self.route2, "route3"]
        stops = [self.stop1, self.stop2, self.stop3]
        
        # Add routes
        for route in routes:
            self.system.add_route(route)
            
        # Add stops in different combinations
        self.system.add_stop_to_route(routes[0], stops[0])  # route1: stop1
        self.system.add_stop_to_route(routes[0], stops[1])  # route1: stop1, stop2
        self.system.add_stop_to_route(routes[1], stops[1])  # route2: stop2
        self.system.add_stop_to_route(routes[1], stops[2])  # route2: stop2, stop3
        self.system.add_stop_to_route(routes[2], stops[0])  # route3: stop1
        self.system.add_stop_to_route(routes[2], stops[2])  # route3: stop1, stop3
        
        # Verify stop1 is in route1 and route3
        routes_with_stop1 = self.system.get_routes_by_stop(stops[0].id)
        assert len(routes_with_stop1) == 2
        assert routes[0] in routes_with_stop1
        assert routes[2] in routes_with_stop1
        
        # Verify stop2 is in route1 and route2
        routes_with_stop2 = self.system.get_routes_by_stop(stops[1].id)
        assert len(routes_with_stop2) == 2
        assert routes[0] in routes_with_stop2
        assert routes[1] in routes_with_stop2
        
        # Remove a stop and verify updates
        self.system.remove_stop_from_route(routes[0], stops[0].id)
        updated_routes = self.system.get_routes_by_stop(stops[0].id)
        assert len(updated_routes) == 1
        assert routes[2] in updated_routes