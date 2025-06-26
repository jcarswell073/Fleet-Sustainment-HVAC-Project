from wordcloud import WordCloud
text = ' '.join(merged['csmp_narrative_summary'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud for CSMP Narrative Summary')
plt.show()
