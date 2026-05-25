import pandas as pd
import matplotlib.pyplot as plt
import os

# Define paths
input_folder = r"H:\Toni_Kroos_Analysis\Raw_Data\Statistics"
output_folder = r"H:\Toni_Kroos_Analysis\Visualizations"
os.makedirs(output_folder, exist_ok=True)

# Function to generate story-like summaries
def generate_story(column, col_mean, col_min, col_max, col_std):
    story = (
        f"{column} reveals interesting patterns. On average, the value hovers around {col_mean:.2f}, "
        f"with a peak of {col_max:.2f} and a low of {col_min:.2f}. The variation (Std Dev: {col_std:.2f}) "
        f"indicates {'consistency' if col_std < 5 else 'fluctuations'} in performance. This highlights "
        f"{'stability' if col_std < 5 else 'changing dynamics'} in the data."
    )
    return story

# Function to create visualizations with story summaries
def create_visualizations_with_stories(data, file_name):
    visualizations = []
    numeric_data = data.select_dtypes(include='number')

    if not numeric_data.empty:
        for column in numeric_data.columns:
            # Calculate summary statistics
            col_mean = numeric_data[column].mean()
            col_min = numeric_data[column].min()
            col_max = numeric_data[column].max()
            col_std = numeric_data[column].std()

            # Generate a story summary
            story = generate_story(column, col_mean, col_min, col_max, col_std)

            # Line Chart with Story Summary
            plt.figure(figsize=(10, 8))
            numeric_data[column].plot(kind='line', marker='o', color='teal', linewidth=2)
            plt.title(f"Trend Analysis: {column} ({file_name})", fontsize=16)
            plt.xlabel("Index")
            plt.ylabel(column)
            plt.grid(alpha=0.5, linestyle='--')

            # Add story as annotation
            plt.gcf().text(0.02, 0.02, story, fontsize=10, wrap=True, color="black")
            plt.tight_layout()
            line_chart_path = os.path.join(output_folder, f"{file_name}_{column}_trend.png")
            plt.savefig(line_chart_path, dpi=300)
            plt.close()
            visualizations.append(line_chart_path)

            # Bar Chart with Story Summary
            plt.figure(figsize=(10, 8))
            numeric_data[column].plot(kind='bar', color='steelblue')
            plt.title(f"Bar Chart: {column} ({file_name})", fontsize=16)
            plt.xlabel("Index")
            plt.ylabel(column)
            plt.grid(alpha=0.5, linestyle='--')

            # Add story as annotation
            plt.gcf().text(0.02, 0.02, story, fontsize=10, wrap=True, color="black")
            plt.tight_layout()
            bar_chart_path = os.path.join(output_folder, f"{file_name}_{column}_bar_chart.png")
            plt.savefig(bar_chart_path, dpi=300)
            plt.close()
            visualizations.append(bar_chart_path)

    return visualizations

# Process each file in the input folder
all_visualizations = {}

for file in os.listdir(input_folder):
    file_path = os.path.join(input_folder, file)
    file_name = os.path.splitext(file)[0]

    if file.endswith(".csv"):
        data = pd.read_csv(file_path)
    elif file.endswith(".xlsx"):
        data = pd.read_excel(file_path)
    else:
        continue

    print(f"Processing file: {file}")
    visualizations = create_visualizations_with_stories(data, file_name)
    all_visualizations[file_name] = visualizations

# Final output message
print(f"Visualizations with story-like summaries saved in: {output_folder}")
