import re

# Define the function to parse the enum definitions and generate unit tests
def generate_enum_unit_tests(input_file, output_file):
    try:
        # Open the input file containing enum definitions
        with open(input_file, 'r') as infile:
            lines = infile.readlines()

        # Prepare the output file for the unit test code
        with open(output_file, 'w') as outfile:
            outfile.write("import static org.junit.jupiter.api.Assertions.assertEquals;\n")
            outfile.write("import org.junit.jupiter.api.Test;\n")
            outfile.write("\n")
            outfile.write("public class EnumTest {\n")

            # Process each line to extract the enum and its values
            for line in lines:
                # Regex to match CID(0, "VALUE")
                match = re.match(r'(\w+)\(([^,]+),\s*\"([^"]+)\"\)', line)
                if match:
                    enum_name = match.group(1)
                    number = match.group(2)
                    value = match.group(3)

                    # Generate a unit test for the current enum
                    outfile.write(f"    @Test\n")
                    outfile.write(f"    public void test{enum_name}() {{\n")
                    outfile.write(f"        assertEquals({enum_name}.get({number}), \"{value}\");\n")
                    outfile.write(f"    }}\n\n")

            outfile.write("}")

        print(f"Unit tests generated successfully in {output_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the input and output files
input_file = "enum_definitions.txt"  # Replace with your input file
output_file = "GeneratedEnumTest.java"  # Replace with your desired output file

# Run the function to generate the tests
generate_enum_unit_tests(input_file, output_file)
