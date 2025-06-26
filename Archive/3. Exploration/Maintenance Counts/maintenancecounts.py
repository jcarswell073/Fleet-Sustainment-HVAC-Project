merged['year'] = merged['date_maintenance_action'].dt.year
merged['month'] = merged['date_maintenance_action'].dt.month
merged['day_of_week'] = merged['date_maintenance_action'].dt.dayofweek

sns.countplot(x='year', data=merged)
plt.title('Distribution by Year')
plt.show()

sns.countplot(x='month', data=merged)
plt.title('Distribution by Month')
plt.show()

sns.countplot(x='day_of_week', data=merged)
plt.title('Distribution by Day of Week')
plt.show()
