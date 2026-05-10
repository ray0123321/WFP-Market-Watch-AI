import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda():
    print("Starting Advanced EDA...")
    if not os.path.exists('feature_engineered_dataset.csv'):
        print("Dataset not found!")
        return
        
    df = pd.read_csv('feature_engineered_dataset.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    sns.set_theme(style="whitegrid")
    
    # Get top 5 commodities for standard charts
    top_commodities = df['commodity'].value_counts().nlargest(5).index
    df_top = df[df['commodity'].isin(top_commodities)]
    
    # 1. Price Trend Graph
    print("Generating Price Trend Graph...")
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df_top, x='date', y='price', hue='commodity')
    plt.title('Price Trend of Top 5 Commodities Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price (PKR)')
    plt.legend(title='Commodity')
    plt.tight_layout()
    plt.savefig('price_trend.png')
    plt.close()
    
    # 2. Seasonal Analysis
    print("Generating Seasonal Analysis Graph...")
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_top, x='month', y='price', hue='commodity')
    plt.title('Seasonal Price Variations by Month (Top 5 Commodities)')
    plt.xlabel('Month')
    plt.ylabel('Price (PKR)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('seasonal_analysis.png')
    plt.close()
    
    # 3. City Comparison
    print("Generating City Comparison Graph...")
    top_commodity = top_commodities[0] 
    plt.figure(figsize=(12, 6))
    df_city = df[df['commodity'] == top_commodity]
    city_avg = df_city.groupby('admin2')['price'].mean().sort_values(ascending=False)
    # Using x and hue as recommended by seaborn deprecation warning
    sns.barplot(x=city_avg.index, y=city_avg.values, hue=city_avg.index, palette='viridis', legend=False)
    plt.title(f'Average Price of {top_commodity} across Cities')
    plt.xlabel('City (admin2)')
    plt.ylabel('Average Price (PKR)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('city_comparison.png')
    plt.close()

    # 4. Correlation Heatmap
    print("Generating Correlation Heatmap...")
    plt.figure(figsize=(10, 8))
    # Select only numeric columns for correlation
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Heatmap of Engineered Features')
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png')
    plt.close()

    # 5. Price Distribution Histogram
    print("Generating Price Distribution Plot...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], bins=50, kde=True, color='purple')
    plt.title('Distribution of Food Prices (Histogram)')
    plt.xlabel('Price (PKR)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('price_distribution.png')
    plt.close()
    
    print("Advanced EDA completed! 5 Plots saved successfully.")

if __name__ == "__main__":
    run_eda()
