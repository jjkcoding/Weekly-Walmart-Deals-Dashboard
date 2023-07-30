# Weekly Walmart Deals Dashboard Project [(Tableau Link)](https://public.tableau.com/app/profile/joshua.kim6929/viz/WeeklyWalmartDealsDashboard/WeeklyWalmartDealsDashboard)

![Weekly Walmart Deals Dashboard](https://github.com/jjkcoding/Weekly-Walmart-Deals-Dashboard/assets/43764400/f67944f2-9a47-425d-951d-e8b0d9e4afb4)


## Project Summary:

* Developed an automated weekly Python web scraper using Selenium to gather weekly deals data from Walmart's website in five sections: Beauty, Electronics, Health and Medicine, Home Improvement, and Personal Care.
* Stored the scraped data in a Google Sheets document for easy access and management.
* Created an interactive Tableau dashboard connected to the Google Sheets displaying key performance indicators (KPIs) all filterable by category.
* Demonstrated the power of web scraping, data integration with Google Sheets, and data visualization through Tableau, providing valuable insights into Walmart's weekly deals.


## Process:

### Web Scraping Walmart with Selenium:
* Used Selenium to navigate Walmart's weekly deals page (https://www.walmart.com/shop/deals/flash-picks) for each category.
* Interacted with web page to get each specific category (Beauty, Electronics, Health and Medicine, Home Improvement, and Personal Care).
* Extracted relevant data, including product name, category, sale price, old price, money saved, percentage saved, and urls.
* Cleaned and exported data into a clean csv file.

### Google Sheets Integration:
* Implemented the Google Sheets API to automatically store the scraped data frame into a Google Sheets document.
* Enabled easy data access and ensured data consistency for further analysis.
* [Google Sheets Link](https://docs.google.com/spreadsheets/d/1BbQbzkmTUUvvSN_lDANqyjx_28B5qNMLKTlxxzsSWF0/edit?usp=sharing)

### Tableau Dashboard Creation:
* Connected the Google Sheets document to Tableau to use the scraped data as a data source.
* Designed an interactive dashboard with various KPIs (like total deals, average percent discount, total money saved, top deals by dollar and percentage, total amount saved by section, and percent saved distribution by category, all filterable by category) and visualizations based on the collected data.
* Allowed users to filter and explore the data dynamically by category.
* [Tableau Link](https://public.tableau.com/app/profile/joshua.kim6929/viz/WeeklyWalmartDealsDashboard/WeeklyWalmartDealsDashboard)


## Conclusion:

Through this project, I learned:

* How to utilize Selenium for web scraping and interacting with web pages to gather specific data from web pages efficiently.
* The process of integrating web-scraped data with Google Sheets, enabling seamless data storage and retrieval.
* The power of Tableau in creating insightful and interactive data visualizations that help users gain valuable insights.
* The importance of automation in data gathering and analysis, facilitating real-time updates and easy data management for better decision-making.
