# JustBid

#### About the application : 

The “JustBid.com” is a web application that acts as an auction site for bidding items.
There can be visitors can just view the items but cannot take any action. There are customers who are the users of the application.
So, the customers who will be registering to the application can place items for auction and other customers who view the item can bid for the items in the list if they are interested. The items to be bid will be having a certain time period(a week). If the item is bid and the owner of the item is satisfied with the bid , the item is labelled as done and the customer who bid with highest amount gets the item. If the item is not bid in the time period, the customer is given a choice to put it resale with different auction price  for another week or the item is removed from the list. If the item has not received any bid twice(two weeks),  the item is marked as not available in the list.
The admin has the functionality to add, verify and manage the customers, items and bids.
This application provides a view of what items are for auction, what items are being bid and who are the customers performing bids at what price and at what time.


#### Instructions to how to download the code:
1.	Go to the github repository and clone the repository to your local application.
2.	Setup the venv
3.	Run “pip install -r requirements.txt”
4.	Perform migrations
```python manage.py makemigrations```   
```python manage.py migrate```
5.	Create super user
 ```python manage.py createsuperuser```
6.	Run the application - 
```python manage.py runserver```
7.	Signup for the application
8.	Login to the application
9.	Add/Edit/Delete/repost the Items for other customer to bid in My Items page
10.	Bid for the Items in the Home Page
11.	Check for the Items you have bid – My Bids Page
12.	Declare a winner for the BID DONE of your items in the My Items  page.
13.	Search for the items available to bid in Home Page.
14.	Rebid the items – My Bids/Home Page.
15.	Perform functionalities such as Edit/View Profile, Change or Reset Password.  
