#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests  # used to send HTTP requests and interact with web pages.
from bs4 import BeautifulSoup  # used for web scraping. It helps parse and extract information from HTML and XML documents.
import numpy as np  # for numerical computing in Python
import pandas as pd  # data manipulation and analysis.
import matplotlib.pyplot as plt  # plotting library.
import seaborn as sns  # Seaborn is another data visualization library built on top of Matplotlib.

# In[2]:


url = 'https://www.flipkart.com/search?q=laptop+under+20000&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_13_na_na_na&as-pos=2&as-type=RECENT&suggestionId=laptop+under+20000%7CLaptops&requestId=391506f8-dfb9-4bb7-8fea-8cdec70a9443&as-searchtext=laptop%20under%20'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup)

# create new page change link
page_link = soup.find('a', class_='ge-49M _2Kfbh8').get('href')
chage_link = 'https://flipkart.com' + page_link
print(chage_link)

# In[3]:


# create empty list to store result of each section

product_name = []
prices = []
totals = []
offer = []
rating = []
processor = []
description = []

# In[4]:


for i in range(1, 51):
    url = f"{chage_link[:-1]}{i}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    box = soup.find('div', class_='_1YokD2 _3Mn1Gg')
    product_details = box.find_all('div', class_='_3pLy-c row')

    for detail in product_details:

        # get product name from page
        name = detail.find('div', class_='_4rR01T')
        if name is not None:
            product_name.append(name.text)
        else:
            product_name.append('N/A')

        # get product price from page
        price = detail.find('div', class_='_30jeq3 _1_WHN1')
        if price is not None:
            prices.append(price.text)
        else:
            prices.append('N/A')

        # get product total price from page
        total = detail.find('div', class_='_3I9_wc _27UcVY')
        if total is not None:
            totals.append(total.text)
        else:
            totals.append('N/A')

        ##get product offer from page
        off = detail.find('div', class_='_3Ay6Sb')
        if off is not None:
            off_span = off.find('span')
            if off_span is not None:
                offer.append(off_span.text)
            else:
                offer.append('N/A')
        else:
            offer.append('N/A')

        ##get product rating from page
        rate = detail.find('div', class_='_3LWZlK')
        if rate is not None:
            rating.append(rate.text)
        else:
            rating.append('N/A')

        # get product processor from page
        pro = detail.find('li', class_='rgWa7D')
        if pro is not None:
            processor.append(pro.text)
        else:
            processor.append('N/A')

        ##get product description from page
        desc = detail.find('ul', class_='_1xgFaf')
        if desc is not None:
            description.append(desc.text)
        else:
            description.append('N/A')

# In[5]:


# Change to dataframe information
df = pd.DataFrame(
    {"Product_Name": product_name, "Total": totals, "Selling_Price": prices, "Offer": offer, "Ratings": rating,
     "Processor": processor, "Description": description})

# In[6]:


# convert to csv file
df.to_csv('laptop_details.csv', index=False)

# In[7]:


df.head(10)

# In[8]:


# dimensions of the DataFrame in the format (rows, columns).
df.shape

# In[9]:


# information about the DataFrame, including the number of non-null values, data types of columns, memory usage, and more.
df.info()

# In[10]:


# create a way to represent missing or unknown data.
df.replace('N/A', np.nan, inplace=True)

# In[11]:


# It returns a Series object that shows the count of null values for each column.
df.isnull().sum()

# In[12]:


# Create method to drop rows containing missing values (NaN). So for this dropna is used to remove rows with NaN values.
df.dropna(subset=['Total', 'Selling_Price', 'Offer'], inplace=True, axis=0)

# In[13]:


df['Total'] = df['Total'].str.replace('₹', '').str.replace(',', '').astype('int')
df['Selling_Price'] = df['Selling_Price'].str.replace('₹', '').str.replace(',', '').astype('int')
df['Offer'] = df['Offer'].str.replace('off', '')

# In[14]:


df.head(10)

# In[15]:


# regular expression (regex) pattern to identify the RAM capacity in GB.
df['RAM'] = df['Description'].str.extract(r'(\d+\s*GB)')
print(df['RAM'].head(10))

# In[16]:


print(df['Product_Name'].head(10))

# In[17]:


# splits each element in the 'Product_Name' column into a list of substrings using the '-' character as a delimiter
df['Product_Name'] = df['Product_Name'].str.split('-')
df['Product_Name'] = df['Product_Name'].str.get(0)
print(df['Product_Name'].head(10))

# In[18]:


# get brand name from product name column
df['Brand'] = df['Product_Name'].str.split()
df['Brand'] = df['Brand'].str.get(0)
print(df['Brand'].head(10))

# In[19]:


# get processor brand from processor column
df['Processor_Brand'] = df['Processor'].str.split()
df['Processor_Brand'] = df['Processor_Brand'].str.get(0)
print(df['Processor_Brand'].head(10))

# In[20]:


# creates a new DataFrame
df = df[['Product_Name', 'Brand', 'RAM', 'Offer', 'Ratings', 'Selling_Price', 'Total', 'Processor_Brand', 'Processor']]

# In[21]:


df.isnull().sum()

# In[22]:


# calculates the average rating from the 'Ratings' column in the DataFrame.
avg_rating = round(df['Ratings'].astype('float').mean(), 1)

# replaces any missing values in the 'Ratings' column of the DataFrame.
df['Ratings'].fillna(avg_rating, inplace=True)
df['Ratings'] = df['Ratings'].astype('float')

# In[23]:


# creates a new DataFrame
df = df[['Product_Name', 'Brand', 'RAM', 'Offer', 'Ratings', 'Selling_Price', 'Total', 'Processor_Brand', 'Processor']]

# In[24]:


df.isnull().sum()

# In[25]:


df.info()

# In[26]:


# clean dataset into csv
df.to_csv('Clean dataset laptop.csv', index=False)

# In[27]:


df.head(10)

# In[28]:


# Now we start Data Analysis and Visulizations


print((f"Total laptops are: {len(df['Product_Name'].unique())}pcs."))

# In[29]:


# finds the top 10 brands with the highest number of products,
# creates a pie chart representing the distribution of products across these brands,
# and displays the chart with brand names, count percentages, and an explode effect for a couple of slices to enhance visibility.

laptop_brand = df.groupby('Brand', as_index=False)['Product_Name'].count().sort_values(by='Product_Name',
                                                                                       ascending=False).head(10)
brand_name = [i.capitalize() for i in laptop_brand['Brand']]  # This way we can capitalized the brand name.
myexplode = [0, 0, 0, 0, 0, 0, 0.1, 0, 0.2, 0]
plt.pie(laptop_brand['Product_Name'], labels=brand_name, explode=myexplode, autopct='%1.1f%%')

plt.title('These Brand are available')
plt.show()

# In[30]:


# Top 10 rating Brands

top10_rating_brand = df.groupby(['Brand'], as_index=False)['Ratings'].mean().round(1).sort_values(by='Ratings',
                                                                                                  ascending=False).head(
    10)
print(f"top10_rating_brand \n\n{top10_rating_brand}")

# In[31]:


# Top processor rating
top_rating_processor = df.groupby('Processor_Brand', as_index=False)['Ratings'].mean().round(1).sort_values(
    by='Ratings', ascending=False)
processor_brands = ['AMD', 'Intel', 'MediaTek', 'Qualcomm']
x = top_rating_processor[top_rating_processor['Processor_Brand'].isin(processor_brands)]

print(f"top_rating_processor \n\n{x}")

# In[32]:


# Chart for Top available processor
plt.figure(figsize=(5, 4))
ax = sns.countplot(x='Processor_Brand', data=df[df['Processor_Brand'].isin(processor_brands)], palette='CMRmap')
plt.title('Top Available Processor', color='g')
plt.show()

# In[33]:


# chart analysis for availablity of laptop using RAM
ram_type = df.groupby('RAM', as_index=False)['Brand'].count().sort_values(by='Brand', ascending=False).head(4)
plt.figure(figsize=(5, 4))  # Chart size
ax = sns.barplot(x='RAM', y='Brand', data=ram_type)
plt.title('These RAM Laptops are available', color='b')
plt.ylabel('Counts')
for bars in ax.containers:
    ax.bar_label(bars, padding=-20)

# In[34]:


# Minimun price of Laptops

min_price_laptop = df.groupby('Product_Name', as_index=False)['Selling_Price'].min().sort_values(by='Selling_Price',
                                                                                                 ascending=True).head(
    10)
print(f"Minimun price of Laptops \n\n{min_price_laptop}")

# In[35]:


# Maximum price of Laptops

max_price_laptop = df.groupby('Product_Name', as_index=False)['Selling_Price'].max().sort_values(by='Selling_Price',
                                                                                                 ascending=False).head(
    10)
print(f"Maximum price of Laptops \n\n{max_price_laptop}")

# In[36]:


df.head(10)

# In[37]:


# Product under 20000
Product_under_20000 = df[df['Selling_Price'] <= 20000]
Product_under_20000 = Product_under_20000[
    ['Product_Name', 'Selling_Price', 'Ratings', 'Processor_Brand', 'RAM', 'Offer']].head(10)
print(Product_under_20000)

# In[ ]:




