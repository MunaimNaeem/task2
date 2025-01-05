



def process_data_with_dict_fromkeys(file_name, skip_lines=3, delimiter=','):
  
    data = {}
    with open(file_name) as file:
        for count, line in enumerate(file):
            if count <= skip_lines:
                
                continue
            elif '%' in line:
                
                names = line.strip('%, \n').split(delimiter)
                data = dict.fromkeys(names, [])
                print("Created dictionary using dict.fromkeys:", data)
                return data


file_name = "1kW_4poles_DO.csv"
data_dict = process_data_with_dict_fromkeys('C:\\Users\\pc\\Desktop\\1kW_4poles_DO.csv')




    # Task 2: Transform string data to float using a lambda function

def process_data_transform_to_float(file_name, skip_lines=3, delimiter=','):
      """
      Reads data from the specified file, processes it, and converts string data to float.

      Args:
          file_name (str): Path to the input file.
          skip_lines (int): Number of lines to skip at the start of the file.
          delimiter (str): Delimiter used in the file.

      Returns:
          dict: Processed data dictionary with float values.
      """
      data = {}

      # Lambda function to convert string to float
      transform_to_float = lambda x: float(x) if x else None

      with open(file_name) as file:
          for count, line in enumerate(file):
              if count <= skip_lines:
                  # Skip initial description lines
                  continue
              elif '%' in line:
                  # Extract variable names and create dictionary with empty lists
                  names = line.strip('%, \n').split(delimiter)
                  data = {name: [] for name in names}
              else:
                  # Process data lines and convert values to float
                  values = line.strip('\n').split(delimiter)
                  for key, value in zip(data.keys(), values):
                      data[key].append(transform_to_float(value))

      return data

  # Task 3: Perform data analysis and compute statistics
def compute_statistics(data_dict):
      """
      Compute basic statistics for each column in the data dictionary.

      Args:
          data_dict (dict): Dictionary containing the data.

      Returns:
          dict: Statistics for each column (mean, min, max).
      """
      import numpy as np

      statistics = {}
      for key, values in data_dict.items():
          # Remove None values for calculations
          clean_values = [v for v in values if v is not None]
          if clean_values:
              statistics[key] = {
                  'mean': np.mean(clean_values),
                  'min': np.min(clean_values),
                  'max': np.max(clean_values),
                  'count': len(clean_values),
                  'std': np.std(clean_values)  # Added standard deviation
              }
          else:
              statistics[key] = {
                  'mean': None,
                  'min': None,
                  'max': None,
                  'count': 0,
                  'std': None
              }
      return statistics

  # Task 4: Visualize and Save Statistics
def sanitize_filename(name):
      """
      Remove invalid characters from a string for safe file naming.

      Args:
          name (str): Original name.

      Returns:
          str: Sanitized name.
      """
      import re
      return re.sub(r'[<>:"/\\|?*]', '_', name)

def visualize_and_save_statistics(statistics, output_file='statistics.json'):
      """
      Visualize statistics and save them to a JSON file.

      Args:
          statistics (dict): Dictionary of computed statistics.
          output_file (str): File path for saving statistics.
      """
      import json
      import matplotlib.pyplot as plt
      import os

      # Ensure the 'plots' directory exists
      os.makedirs("plots", exist_ok=True)

      # Save statistics to a JSON file
      with open(output_file, 'w') as file:
          json.dump(statistics, file, indent=4)

      # Visualization
      for key, stats in statistics.items():
          if stats['count'] > 0:  # Only plot if there is valid data
              try:
                  values = [stats['mean'], stats['min'], stats['max']]
                  labels = ['Mean', 'Min', 'Max']
                  plt.figure()
                  plt.bar(labels, values)
                  plt.title(f"Statistics for {key}")
                  plt.ylabel("Value")
                  sanitized_key = sanitize_filename(key)
                  plt.savefig(os.path.join("plots", f"{sanitized_key}_statistics.png"))
                  print(f"Plot saved for {key} as {sanitized_key}_statistics.png")
                  plt.show()  # Display the plot interactively
                  plt.close()  # Close the figure to free memory
              except Exception as e:
                  print(f"Error creating plot for {key}: {e}")
          else:
              print(f"No valid data for {key}, skipping plot.")

  # Task 5: Detect Anomalies in Data
def detect_anomalies(data_dict, statistics):
      """
      Detect anomalies in the data based on a z-score threshold.

      Args:
          data_dict (dict): Dictionary containing the data.
          statistics (dict): Dictionary containing computed statistics.

      Returns:
          dict: Anomalies detected for each column.
      """
      import numpy as np

      anomalies = {}
      threshold = 3  # Z-score threshold for anomaly detection

      for key, values in data_dict.items():
          clean_values = np.array([v for v in values if v is not None])
          if len(clean_values) > 0:
              mean = statistics[key]['mean']
              std = statistics[key]['std']
              if std is not None and std > 0:
                  z_scores = (clean_values - mean) / std
                  anomalies[key] = clean_values[np.abs(z_scores) > threshold].tolist()
              else:
                  anomalies[key] = []
          else:
              anomalies[key] = []

      return anomalies


file_name = "1kW_4poles_DO.csv"
data_dict = process_data_transform_to_float('C:\\Users\\pc\\Desktop\\1kW_4poles_DO.csv')

  # Compute statistics for the processed data
stats = compute_statistics(data_dict)

  # Display the statistics
print("Statistics for the data:")
for key, value in stats.items():
      print(f"{key}: {value}")

  # Visualize and save the statistics
visualize_and_save_statistics(stats)

  # Detect anomalies in the data
anomalies = detect_anomalies(data_dict, stats)

  # Display anomalies
print("\nAnomalies detected in the data:")
for key, anomaly_values in anomalies.items():
      if anomaly_values:
          print(f"{key}: {anomaly_values}")
      else:
          print(f"{key}: No anomalies detected.")





