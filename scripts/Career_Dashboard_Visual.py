# Separate Dashboard Visuals for Club, National, and Individual Performance
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the career statistics Excel file
career_stats_path = r'H:\Toni_Kroos_Analysis\Raw_Data\Statistics\career_stats.xlsx'
career_stats = pd.read_excel(career_stats_path, sheet_name=None)

# Load individual sheets for further processing
club_career_stats = career_stats['Club career']
international_career_stats = career_stats['International career']
honours_stats = career_stats['Honours']

# CLUB PERFORMANCE VISUALS
fig, axes = plt.subplots(2, 2, figsize=(32, 26))
fig.suptitle('Toni Kroos - Club Performance Overview', fontsize=28, fontweight='bold')

# Plot 1: Club Career Appearances Over Seasons
ax1 = axes[0, 0]
club_career_summary = club_career_stats.groupby('season')['league'].count().reset_index()
sns.lineplot(data=club_career_summary, x='season', y='league', marker='o', ax=ax1, color='b')
ax1.set_title('Club Career Appearances Over Seasons', fontsize=18, fontweight='bold')
ax1.set_xlabel('Season')
ax1.set_ylabel('Number of Appearances')
ax1.tick_params(axis='x', rotation=45)

# Plot 2: Goals vs Assists for Club Career Over Seasons
ax2 = axes[0, 1]
club_goals_assists = club_career_stats.groupby('season').agg({'league.1': 'sum', 'Unnamed: 4': 'sum'}).reset_index()
sns.lineplot(data=club_goals_assists, x='season', y='league.1', marker='o', label='Goals', ax=ax2, color='b')
sns.lineplot(data=club_goals_assists, x='season', y='Unnamed: 4', marker='s', label='Assists', ax=ax2, color='g')
ax2.set_title('Club Career Goals vs Assists Over Seasons', fontsize=18, fontweight='bold')
ax2.set_xlabel('Season')
ax2.set_ylabel('Count')
ax2.legend()
ax2.tick_params(axis='x', rotation=45)

# Plot 3: Minutes Played Per Season
ax3 = axes[1, 0]
if 'minutes_played' in club_career_stats.columns:
    minutes_played_data = club_career_stats.groupby('season')['minutes_played'].sum().reset_index()
else:
    minutes_played_data = pd.DataFrame({'season': club_career_stats['season'].unique(), 'minutes_played': [0] * len(club_career_stats['season'].unique())})
sns.barplot(data=minutes_played_data, x='season', y='minutes_played', hue='season', ax=ax3, legend=False, palette='Oranges_d')
ax3.set_title('Minutes Played Per Season', fontsize=18, fontweight='bold')
ax3.set_xlabel('Season')
ax3.set_ylabel('Minutes Played')
ax3.tick_params(axis='x', rotation=45)

# Plot 4: Average Distance Covered Per Match (Placeholder Data)
ax4 = axes_club[1, 1]
distance_data = [11.5, 11.8, 11.6, 12.0, 11.9, 12.1, 11.7, 12.2]
seasons = ['2013/14', '2014/15', '2015/16', '2016/17', '2017/18', '2018/19', '2019/20', '2020/21']
sns.lineplot(x=seasons, y=distance_data, marker='o', ax=ax4, color='purple')
ax4.set_title('Average Distance Covered Per Match (km)', fontsize=18, fontweight='bold')
ax4.set_xlabel('Season')
ax4.set_ylabel('Distance (km)')
ax4.tick_params(axis='x', rotation=45)

plt.tight_layout(rect=[0.1, 0.1, 0.9, 0.9])
plt.show(block=False)

# NATIONAL TEAM PERFORMANCE VISUALS
fig_national, axes_national = plt.subplots(2, 2, figsize=(24, 18))
fig_national.suptitle("Toni Kroos - National Team Performance Overview", fontsize=28, fontweight='bold')

# Plot 1: National Team Goals Over the Years
ax5 = axes_national[0, 0]
national_goals_summary = international_career_stats.groupby('Year')['Goals'].sum().reset_index()
sns.barplot(data=national_goals_summary, x='Year', y='Goals', hue='Year', ax=ax5, legend=False, palette='Blues_d')
ax5.set_title('National Team Goals Over the Years', fontsize=18, fontweight='bold')
ax5.set_xlabel('Year')
ax5.set_ylabel('Number of Goals')
ax5.tick_params(axis='x', rotation=45)

# Plot 2: Key Matches and Milestones Timeline
ax6 = axes_national[0, 1]
years = [2013, 2014, 2016, 2017, 2018]
key_milestones = ['2013 UCL Win', '2014 World Cup Win', '2016 UCL Win', '2017 UCL Win', '2018 UCL Win']
ax6.plot(years, [1, 2, 3, 4, 5], marker='o', color='r', linestyle='-', linewidth=2)
for i, milestone in enumerate(key_milestones):
    ax6.text(years[i], i + 0.2, milestone, fontsize=14, ha='center')

plt.tight_layout(rect=[0.1, 0.1, 0.9, 0.9])
plt.show()

# INDIVIDUAL PERFORMANCE AND HONORS VISUALS
fig_individual, axes_individual = plt.subplots(2, 2, figsize=(24, 18))
fig_individual.suptitle("Toni Kroos - Individual Performance and Honors Overview", fontsize=28, fontweight='bold')

# Plot 1: Distribution of Honors Won
ax9 = axes_individual[0, 0]
honours_summary = honours_stats.melt(var_name='Club/National', value_name='Honors')
honours_summary = honours_summary.dropna().reset_index(drop=True)
honours_counts = honours_summary['Club/National'].value_counts()
ax9.pie(honours_counts, labels=honours_counts.index, autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'black'}, colors=sns.color_palette('Set2'))
ax9.set_title('Distribution of Honors Won by Toni Kroos', fontsize=18, fontweight='bold')

# Plot 2: Passing Accuracy Heatmap (Placeholder Data)
ax10 = axes_individual[0, 1]
passing_data = [[95, 93, 91], [92, 90, 94], [93, 94, 92]]
sns.heatmap(passing_data, annot=True, cmap='RdYlBu', ax=ax10)
ax10.set_title('Passing Accuracy Heatmap (Placeholder)', fontsize=18, fontweight='bold')

# Plot 3: Assist Types Breakdown (Placeholder Data)
ax11 = axes_individual[1, 0]
assist_types = ['Through Ball', 'Cross', 'Short Pass', 'Long Pass']
assist_counts = [25, 40, 30, 20]
sns.barplot(x=assist_types, y=assist_counts, hue=assist_types, ax=ax11, legend=False, palette='husl')
ax11.set_title('Assist Types Breakdown', fontsize=18, fontweight='bold')
ax11.set_xlabel('Assist Type')
ax11.set_ylabel('Number of Assists')

# Plot 4: Estimated Pass Completion Rate Over Seasons
ax12 = axes_individual[1, 1]
seasons_subset = club_career_stats['season'].dropna().unique()[:8]
pass_completion_rate_subset = [91, 92, 90, 93, 94, 91, 92, 93]
sns.barplot(x=seasons_subset, y=pass_completion_rate_subset, hue=seasons_subset, ax=ax12, legend=False, palette='Greens_d')
ax12.set_title('Estimated Pass Completion Rate Over Seasons', fontsize=18, fontweight='bold')
ax12.set_xlabel('Season')
ax12.set_ylabel('Pass Completion Rate (%)')
ax12.tick_params(axis='x', rotation=45)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
