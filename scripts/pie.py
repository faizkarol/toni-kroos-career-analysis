import matplotlib.pyplot as plt

# Data for the chart
milestones = [
    "Youth Career Debut", "Hansa Rostock U19 Debut", "Bayern Munich U19 Debut",
    "Bayern Munich II Debut", "Professional Debut", "International Debut",
    "World Cup Victory", "Real Madrid Transfer", "First Goal with Madrid",
    "International Retirement", "600th Club Match"
]
years = [2004, 2005, 2006, 2007, 2007, 2010, 2014, 2014, 2014, 2021, 2023]

# Create the chart
plt.figure(figsize=(10, 6), facecolor="none")
plt.barh(milestones, years, color="#4682B4", alpha=0.8)  # Steel blue for visibility

# Add chart elements
plt.title("Career Milestones Overview", fontsize=16, color="white")
plt.xlabel("Date", fontsize=12, color="white")
plt.ylabel("Milestones", fontsize=12, color="white")

# Customize axis styles for better visibility
plt.xticks(color="white")
plt.yticks(color="white")
plt.gca().spines["bottom"].set_color("white")
plt.gca().spines["left"].set_color("white")
plt.gca().spines["top"].set_color("none")
plt.gca().spines["right"].set_color("none")

# Save the chart with transparent background
plt.tight_layout()
plt.savefig("enhanced_milestone_chart.png", transparent=True)
plt.close()
