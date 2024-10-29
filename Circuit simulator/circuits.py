import matplotlib.pyplot as plt

class Resistor:
    def __init__(self, resistance, config="series"):
        self.resistance = resistance
        self.config = config  # "series" or "parallel"

class VoltageSource:
    def __init__(self, voltage):
        self.voltage = voltage

class Circuit:
    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def total_resistance(self):
        """Calculate the total resistance based on series and parallel configurations."""
        series_resistances = [comp.resistance for comp in self.components if isinstance(comp, Resistor) and comp.config == "series"]
        parallel_resistances = [comp.resistance for comp in self.components if isinstance(comp, Resistor) and comp.config == "parallel"]

        # Calculate series resistance by summing all resistances in series
        total_series_resistance = sum(series_resistances)

        # Calculate parallel resistance by summing reciprocals
        if parallel_resistances:
            reciprocal_sum = sum(1 / r for r in parallel_resistances)
            total_parallel_resistance = 1 / reciprocal_sum if reciprocal_sum != 0 else float('inf')
        else:
            total_parallel_resistance = 0

        # Total resistance is the sum of series and equivalent parallel resistance
        return total_series_resistance + total_parallel_resistance

    def calculate_current(self):
        # Find the first VoltageSource in the list
        voltage_source = next((comp for comp in self.components if isinstance(comp, VoltageSource)), None)
        if voltage_source is None:
            print("No voltage source in the circuit.")
            return None
        total_resistance = self.total_resistance()
        if total_resistance > 0:
            return voltage_source.voltage / total_resistance
        return 0

    def visualize_circuit(self):
        component_names = [f"{type(comp).__name__}" for comp in self.components]
        voltages = [comp.voltage if isinstance(comp, VoltageSource) else self.calculate_current() * comp.resistance for comp in self.components]
        
        plt.bar(component_names, voltages, color="blue")
        plt.xlabel("Component")
        plt.ylabel("Voltage (V)")
        plt.title("Voltage across Circuit Components")
        plt.show()

# Main function to run the simulator with user input
def main():
    circuit = Circuit()

    # Get user input for voltage sources
    num_voltage_sources = int(input("Enter the number of voltage sources: "))
    for i in range(num_voltage_sources):
        voltage = float(input(f"Enter the voltage for voltage source {i + 1} (in volts): "))
        circuit.add_component(VoltageSource(voltage))

    # Get user input for resistors
    num_resistors = int(input("Enter the number of resistors: "))
    for i in range(num_resistors):
        resistance = float(input(f"Enter the resistance for resistor {i + 1} (in ohms): "))
        config = input("Is this resistor in series or parallel? (Enter 'series' or 'parallel'): ").strip().lower()
        circuit.add_component(Resistor(resistance, config))

    # Calculate and display results
    current = circuit.calculate_current()
    print("Total Current in the Circuit:", current, "A")

    # Visualize the circuit
    circuit.visualize_circuit()

# Run the program
if __name__ == "__main__":
    main()