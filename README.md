# Art in the Age of Machine Learning
### Predictive Analytics for Restaurants

#### Project Scope

The restaurant industry operates with notoriously thin operating margins, typically dropping around 5% of total revenue to their bottom lines. For every $1.00 in sales, approximately $0.30 - $0.35 will likely go to cost of goods (e.g. raw ingredients, dry goods, alcohol) while an additional $0.30 - $0.35 will go to labor, leaving roughly $0.30 - $0.40 to cover overhead (rent, insurance, utilities, equipment rentals, waste management, accounting, marketing) and provide a return on capital, to the extent there is any excess after covering all the costs.

An accurate sales forecast provides several avenues of cost saving + revenue expansion to restaurants:

* **Labor Optimization** | Minimize labor hours on slow nights while maintaining appropriate staffing levels on busier nights.
* **Minimize Food Waste** | More precise daily prep levels to help limit food waste.
* **Lean Inventory** | Inventory is a drag on cash flow and high levels of inventory of fresh goods can lead to spoilage and food waste.
* **Marketing Initiatives** | Maximize marketing dollars by targeting slow nights and weeks.

Using real sales data from a two-star restaurant located in Brooklyn, NY, this is a pilot project exploring what an end-to-end restaurant sales forecasting tool utilizing machine learning would entail.

#### Data Sources
* **Restaurant Sales Data** | Restaurant sales and guest counts ("covers") were downloaded directly from the restuarant's Point of Sale ("POS") on a check-by-check basis from 1/1/2017 through 06/30/2019, then aggregated into nightly totals covering the Dinner period only.

* **Weather Data** | Weather data was accessed via the DarkSky API. The source code for the API call can be found [here](https://github.com/maks-p/restaurant_sales_forecasting/blob/master/weather.py "weather.py"). The latitude and longitude for the restuarant, required to access the weather data, is accessed via the Yelp API - the source code for this API call is found [here](https://github.com/maks-p/restaurant_sales_forecasting/blob/master/restaurant_info.py "restaurant_info.py").

#### Restaurant Background

The subject is a two-star restaurant located in Brooklyn, NY. It has a patio that adds a substantial amount of seats. The subject is performing extremely well, earning $5.84 MM in net sales in 2018 on 78,000 covers.

The following two charts demonstrate the restaurant's performance on a monthly basis:

<p float="left">
  <img src="https://user-images.githubusercontent.com/42282874/60995179-ffa7a000-a31f-11e9-80ce-464b11728c0f.png" width="400" />
  <img src="https://user-images.githubusercontent.com/42282874/60995178-ffa7a000-a31f-11e9-9e4c-40493f248ae5.png" width="400" /> 
</p>

With more seating available during the warmer months, there is clear seasonality present. And like most restaurants, the subject is busiest on weekends:

<p float="left">
  <img src="https://user-images.githubusercontent.com/42282874/60994592-d20e2700-a31e-11e9-8c62-8226d3387769.png" width="400" />
  <img src="https://user-images.githubusercontent.com/42282874/60994593-d20e2700-a31e-11e9-95b7-ee228e4adc48.png" width="400" /> 
</p>

The following heatmap shows Average Sales for the restaurant by Day of Week & Month:

![heatmap](https://user-images.githubusercontent.com/42282874/61073078-9b99e000-a3e2-11e9-84cf-de5cd439a12a.png)

In 2018, the last full year of operations, the subject averaged nightly sales of $16,170, with a standard deviation of $2,606.

#### Baseline Linear Regression

A simple Linear Regression Model that accounts for the outside space being open, closed days, and day of week (as dummy variables) performs fairly well, and provides a jumping off point for more extensive feature engineering, including weather data.

```
Train R-Squared:   0.7652830449744104
Test R-Squared:   0.7985732635793398 
Root Mean Squared Error:  1392.6958027653395
```

#### Correlation

A quick look at the correlation coefficients between sales & temperature does imply a meaningful correlation between the two, though this is likely largely caused by the presense of additional outdoors seating in warm weather.

```
{0: 0.6067494091067502,
 1: 0.5648085035371838,
 2: 0.5217618281364986,
 3: 0.5985487427152698,
 4: 0.6526160966680253,
 5: 0.6285813402808068,
 6: 0.5558958668516343}
 ```
 
![download (1)](https://user-images.githubusercontent.com/42282874/61075753-b0797200-a3e8-11e9-8a76-729d48d2da34.png)

