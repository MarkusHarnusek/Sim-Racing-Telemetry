import telemetry.f1_2020 as f1_2020

def main():
    try:
        while True:
            data = f1_2020.run()
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")

if __name__ == "__main__":
    main()