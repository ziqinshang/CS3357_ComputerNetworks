# CS3307 Object-Oriented Design and Analysis Group 61
## Interactive food-ordering system : Description
### Required features:
#### 1.Account Setting
##### - Initialization of chef/waiter ID and table ID
#### 2.Ordering Pages
##### - Show customers the dishes name with photos and prices
##### - “Hurry Up!” and “Need Assistance” choices when waiting for the orders
##### - After choosing “Hurry Up!”, the order will move ahead in the ordering queue
##### - After choosing “Need Assistance”, a message will be sent to a waiter
#### 3.Ordering System
##### - Line up customers orders and collect waiting times of each table
##### - when all orders have been served then stop and discard data until the new order from the same table
#### 4.Payment/Tipping System
##### - After the order has finished, Table ID can give the Waiter ID some amount of tips (by percentage or by amount)
#### 5.Waiter/Chef System
##### - View the cooking order from the ordering system
##### - Waiter may get a “Need Assistance” message from a table
##### - Chef presses “Finish!” button to let waiter know the order is ready
### Optional features:
#### 1.Time-optimization
##### - Set prerequisites in advance for the chef that he may finish some orders at the same time. For example: table 1,2,3,4 all order French fries, to reduce waiting time, chef could put more fries at one time
#### 2.Rating
##### - According to how much time waiting and service, the system could recommend to rate this service after they pay for the bill
### Wish-list features:
#### 1.Browsing the evaluation
##### - Users can view the previous users' evaluation of the dish
#### 2.Payment system
##### - There may be 3 options for customers to pay: Cash,VISA/MasterCard, apple pay. 

## Code Implementation
### Driver Code
#### 1.**main.cpp**
### UI Implementation (Qt 5.12.8)
#### 1.Payment/Tipping System UI: **checkoutwindow.h** **checkoutwindow.cpp**
#### 2.Ordering Pages, Menu UI: **dialog.h** **dialog.cpp**
#### 3.Ordering Pages, Customer UI: **mainwindow.h** **mainwindow.cpp**
#### 4.Waiter/Chef System: **restaurant.h** **restaurant.cpp**
#### 5.UI Structure and Formation: **checkoutwindow.ui** **dialog.ui** **mainwindow.ui** **restaurant.ui**
### Core Functionalities Implementation (C++ Standard Library)
#### 1.Ordering System Class: **order.h** **order.cpp** **orderqueue.h** **orderqueue.cpp**
#### 2.Account Setting: **Table.h** **Table.cpp**
#### 3.Ordering Pages, Dish Initialization: **Dish.h** **Dish.cpp**

## Known & Existing Bugs
### 1. OrderQueue Display @ Restaurant End
#### Description: The only way to refresh/update the OrderQueue Display at Restaurant End is to add a new order in dialog page, i.e. append a new order to orderqueue, other buttons such as "REFRESH" in restaurant page, "HURRY" in mainwindow page, "FINISH" in restaurant page will not trigger refresh the display. However, the internal queue structure is modified as desired, to view any changes made by above bottons, please submit a new order in dialog end.
#### Trigger: Press "SUBMIT" button at dialog UI
#### Potential Reason: The problem with the internal orderqueue pointer structure, during debugging, the signal/slots works as expected.
### 2. Order Generation @ Entire System
#### Description: When generating a new order, i.e. pressing + - button in dialog page, it is ok to make the items display on the right changes as desired, and it is also ok to create a new order by "SUBMIT" botton that contains a dish that has never been added before. However, after the order is submitted, the items display on the dialog page will not clear, and the dishs ordered before must exist at least one. For example, if you have two coffees in the item display, and you submitted this order, when you are trying to create another new order by pressing "submit", you can delete one coffee, but you must leave one in the display, otherwise the system will crash. This bug applies to other dishes too. Super weird bug, limited lots of functionality.
#### Trigger: Press "SUBMIT" button at dialog UI
#### Potential Reason: UNKNOWN
