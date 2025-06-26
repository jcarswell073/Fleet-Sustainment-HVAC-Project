# Line plot of Total Material Cost over time
time_series = hvacdata.groupby(hvacdata['date_maintenance_action'].dt.to_period('M'))['total_material_cost'].sum().reset_index()
time_series['date_maintenance_action'] = time_series['date_maintenance_action'].dt.to_timestamp()

plt.figure(figsize=(12, 6))
sns.lineplot(x='date_maintenance_action', y='total_material_cost', data=time_series)
plt.title('Total Material Cost Over Time')
plt.xlabel('Date')
plt.ylabel('Total Material Cost')
plt.show()
