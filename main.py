from src.collectors.maps_api import MapsAPICollector


def run_single_example():
    print("\n===== SINGLE ORIGIN–DESTINATION EXAMPLE =====")

    origin = "37.7749,-122.4194"        # San Francisco
    destination = "37.8044,-122.2711"   # Oakland

    collector = MapsAPICollector()
    result = collector.run_for_one_pair(origin, destination, save_raw=True)

    print("Origin      :", result["origin"])
    print("Destination :", result["destination"])
    print("Distance    :", result["distance_text"])
    print("Duration    :", result["duration_text"])


def run_batch_example():
    print("\n===== BATCH EXAMPLE =====")

    pairs = [
        ("San Francisco, CA", "San Jose, CA"),
        ("New York, NY", "Jersey City, NJ"),
        ("Los Angeles, CA", "Santa Monica, CA"),
    ]

    collector = MapsAPICollector()
    results = collector.run_batch(pairs, save_raw=True)

    for idx, res in enumerate(results, start=1):
        print("\n--- Pair #{} ---".format(idx))
        print("Origin      :", res["origin"])
        print("Destination :", res["destination"])
        print("Distance    :", res["distance_text"])
        print("Duration    :", res["duration_text"])


def main():
    print("Starting Google Maps collection pipeline...")
    run_single_example()
    run_batch_example()
    print("\nDone.\n")


if __name__ == "__main__":
    main()