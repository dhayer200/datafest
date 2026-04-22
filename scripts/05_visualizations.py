import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

if not os.path.exists("outputs/focus_diabetes.parquet"):
    print("Run 04_focus_analysis.py first to create focus_diabetes.parquet")
    exit(1)

focus = pd.read_parquet("outputs/focus_diabetes.parquet")

sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "figure.figsize": (10, 6),
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

palette = {"Urban": "#2E86AB", "Rural": "#E84855"}
colors = {"Urban": "#2E86AB", "Rural": "#E84855", "Missing": "#CCCCCC"}

print("Creating visualizations...\n")

# ========== CHART 1: HEATMAP — Gap days by geography × barrier ==========
fig, ax = plt.subplots(figsize=(8, 5))

# Build pivot table for heatmap
heatmap_data = []
for geo in ['Urban', 'Rural']:
    for barrier in [False, True]:
        subset = focus[(focus['geography'] == geo) & (focus['has_transport_barrier'] == barrier)]
        if len(subset) > 0:
            median_gap = subset['median_gap_days'].median()
            heatmap_data.append({
                'Geography': geo,
                'Barrier Status': 'Has Barrier' if barrier else 'No Barrier',
                'Median Gap (days)': median_gap
            })

heatmap_df = pd.DataFrame(heatmap_data)
heatmap_pivot = heatmap_df.pivot(index='Geography', columns='Barrier Status', values='Median Gap (days)')
heatmap_pivot = heatmap_pivot[['No Barrier', 'Has Barrier']]  # Reorder columns

sns.heatmap(heatmap_pivot, annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': 'Days'},
            linewidths=1, linecolor='white', ax=ax, vmin=40, vmax=100)

ax.set_title('Gap between diabetes appointments: geography matters more than transportation',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Transportation Barrier Status', fontsize=12, fontweight='bold')
ax.set_ylabel('Geography', fontsize=12, fontweight='bold')

sns.despine()
plt.tight_layout()
plt.savefig('outputs/plot_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: outputs/plot_heatmap.png")
plt.close()

# ========== CHART 2: WAFFLE — Rural patients with/without/missing barrier data ==========
fig, ax = plt.subplots(figsize=(10, 3))

rural = focus[focus['geography'] == 'Rural'].drop_duplicates('patientdurablekey')
rural_has_barrier = len(rural[rural['has_transport_barrier'] == True])
rural_no_barrier = len(rural[rural['has_transport_barrier'] == False])
rural_missing = len(rural[rural['has_transport_barrier'].isna()])

# Normalize to 100 for visual clarity
total_rural = rural_has_barrier + rural_no_barrier + rural_missing
pct_has = int(round(100 * rural_has_barrier / total_rural))
pct_no = int(round(100 * rural_no_barrier / total_rural))
pct_missing = 100 - pct_has - pct_no

# Create horizontal stacked bar
categories = ['Rural patients']
has_barrier_vals = [pct_has]
no_barrier_vals = [pct_no]
missing_vals = [pct_missing]

ax.barh(categories, has_barrier_vals, left=0, label=f'Has barrier (n={rural_has_barrier})',
        color='#E84855', edgecolor='white', linewidth=2)
ax.barh(categories, no_barrier_vals, left=pct_has, label=f'No barrier (n={rural_no_barrier})',
        color='#2E86AB', edgecolor='white', linewidth=2)
ax.barh(categories, missing_vals, left=pct_has+pct_no, label=f'Missing data (n={rural_missing})',
        color='#CCCCCC', edgecolor='white', linewidth=2)

# Annotations on each segment
ax.text(pct_has/2, 0, f'{pct_has}%', va='center', ha='center', fontweight='bold', fontsize=12, color='white')
ax.text(pct_has + pct_no/2, 0, f'{pct_no}%', va='center', ha='center', fontweight='bold', fontsize=12, color='white')
ax.text(pct_has + pct_no + pct_missing/2, 0, f'{pct_missing}%', va='center', ha='center', fontweight='bold', fontsize=12, color='#333')

ax.set_xlim(0, 100)
ax.set_xlabel('Percentage of rural patients', fontsize=12, fontweight='bold')
ax.set_title('41% of rural patients can\'t be assessed for transportation barriers',
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False, fontsize=10)

sns.despine(left=True, bottom=True)
ax.set_yticks([])
plt.tight_layout()
plt.savefig('outputs/plot_missing.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: outputs/plot_missing.png")
plt.close()

# ========== CHART 3: DUMBBELL — Journey duration: Urban vs Rural ==========
fig, ax = plt.subplots(figsize=(10, 5))

dumbbell_data = []
for geo in ['Urban', 'Rural']:
    for barrier in [False, True]:
        subset = focus[(focus['geography'] == geo) & (focus['has_transport_barrier'] == barrier)]
        if len(subset) > 0:
            median_duration = subset['duration_days'].median()
            dumbbell_data.append({
                'Group': f"{geo}\n({'Barrier' if barrier else 'No barrier'})",
                'Duration': median_duration,
                'Geography': geo,
                'Barrier': barrier
            })

dumbbell_df = pd.DataFrame(dumbbell_data)
dumbbell_df['y_pos'] = range(len(dumbbell_df))

# Draw horizontal lines connecting urban and rural
y_urban_no = dumbbell_df[(dumbbell_df['Geography'] == 'Urban') & (dumbbell_df['Barrier'] == False)]['y_pos'].values[0]
y_rural_no = dumbbell_df[(dumbbell_df['Geography'] == 'Rural') & (dumbbell_df['Barrier'] == False)]['y_pos'].values[0]

x_urban_no = dumbbell_df[(dumbbell_df['Geography'] == 'Urban') & (dumbbell_df['Barrier'] == False)]['Duration'].values[0]
x_rural_no = dumbbell_df[(dumbbell_df['Geography'] == 'Rural') & (dumbbell_df['Barrier'] == False)]['Duration'].values[0]

ax.plot([x_urban_no, x_rural_no], [y_urban_no, y_rural_no], 'k-', linewidth=2, alpha=0.3, zorder=1)

# Plot points
for idx, row in dumbbell_df.iterrows():
    color = '#2E86AB' if row['Geography'] == 'Urban' else '#E84855'
    ax.scatter(row['Duration'], row['y_pos'], s=200, color=color, edgecolor='white', linewidth=2, zorder=2)
    ax.text(row['Duration'] + 20, row['y_pos'], f"{row['Duration']:.0f}d",
            va='center', fontsize=10, fontweight='bold')

ax.set_yticks(dumbbell_df['y_pos'])
ax.set_yticklabels(dumbbell_df['Group'], fontsize=11)
ax.set_xlabel('Journey duration (days)', fontsize=12, fontweight='bold')
ax.set_title('Rural diabetes patients have shorter, more episodic care journeys',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlim(150, 850)
ax.grid(axis='x', alpha=0.3)

sns.despine(left=True)
plt.tight_layout()
plt.savefig('outputs/plot_journeys.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: outputs/plot_journeys.png")
plt.close()

print("\n" + "=" * 80)
print("VISUALIZATIONS COMPLETE")
print("=" * 80)
print("Charts saved to outputs/:")
print("  - plot_heatmap.png (gap days by geography and barrier)")
print("  - plot_missing.png (rural data completeness)")
print("  - plot_journeys.png (journey duration comparison)")
