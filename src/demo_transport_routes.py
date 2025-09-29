"""
This script demonstrates the functionality of a public transport route system.
"""
from transport_routes import TransportRouteSystem, Stop

def create_example_system():
    """Creates a sample system with multiple routes and stops"""
    system = TransportRouteSystem()
    
    # Create sample routes (simulating bus routes)
    routes = ["R1", "R2", "R3"]  # Routes 1, 2 and 3
    for route in routes:
        system.add_route(route)
        print(f"Route {route} created")
    
    # Create stops for each route
    stops = {
        "R1": [
            Stop("EST-01", "Central Station"),
            Stop("PAR-02", "Main Park"),
            Stop("MER-03", "Central Market"),
            Stop("HOS-04", "General Hospital")
        ],
        "R2": [
            Stop("EST-01", "Central Station"),
            Stop("UNI-05", "University"),
            Stop("BIB-06", "Public Library"),
            Stop("PAR-02", "Main Park")
        ],
        "R3": [
            Stop("EST-01", "Central Station"),
            Stop("MER-03", "Central Market"),
            Stop("CEN-07", "Shopping Center"),
            Stop("AER-08", "Airport")
        ]
    }
    
    # Add stops to routes
    for route, stops in stops.items():
        print(f"\nAdding stops to route {route}:")
        for stop in stops:
            system.add_stop_to_route(route, stop)
            print(f"  - Added stop: {stop.name} (ID: {stop.id})")
    
    return system

def show_routes_by_stop(system, stop_id):
    """Shows all routes that pass through a specific stop"""
    routes = system.get_routes_by_stop(stop_id)
    print(f"\nRoutes passing through stop {stop_id}:")
    for route in routes:
        print(f"  - Route {route}")
        stops = system.get_stops_in_route(route)
        print("    Stops in this route:")
        for stop in stops:
            print(f"    * {stop.name} (ID: {stop.id})")

def main():
    print("Initializing public transport route system...")
    system = create_example_system()
    
    # Demonstrate route search by stop
    print("\n=== Connection Analysis ===")
    
    # Find routes passing through Central Station
    show_routes_by_stop(system, "EST-01")
    
    # Find routes passing through Main Park
    show_routes_by_stop(system, "PAR-02")
    
    # Find routes passing through Central Market
    show_routes_by_stop(system, "MER-03")
    
    # Demonstrate stop removal
    print("\n=== Route Modification ===")
    print("Removing 'Main Park' stop from route R1...")
    system.remove_stop_from_route("R1", "PAR-02")
    
    # Verify updated routes
    print("\nVerifying updated routes passing through Main Park:")
    show_routes_by_stop(system, "PAR-02")

if __name__ == "__main__":
    main()