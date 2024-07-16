import pandas as pd
import sys

def csv_to_excel(csv_file, excel_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Write the DataFrame to an Excel file
    df.to_excel(excel_file, index=False)
    print(f"CSV file '{csv_file}' has been successfully converted to Excel file '{excel_file}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_excel.py <input_csv_file> <output_excel_file>")
    else:
        input_csv_file = sys.argv[1]
        output_excel_file = sys.argv[2]
        csv_to_excel(input_csv_file, output_excel_file)