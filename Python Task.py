def process_data_with_dict_fromkeys(file_name, skip_lines=3, delimiter=','):
  
    data = {}
    with open(file_name) as file:
        for count, line in enumerate(file):
            if count <= skip_lines:
                # Skip initial description lines
                continue
            elif '%' in line:
                # Extract variable names and create dictionary using dict.fromkeys
                names = line.strip('%, \n').split(delimiter)
                data = dict.fromkeys(names, [])
                print("Created dictionary using dict.fromkeys:", data)
                return data

# Replace 'your_file_path.csv' with the actual file path when running.
file_name = "1kW_4poles_DO.csv"
data_dict = process_data_with_dict_fromkeys('C:\\Users\\pc\\Desktop\\1kW_4poles_DO.csv')
