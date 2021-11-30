//
//  main.cpp
//  CS3307Project
//
//  Created by David Shang on 2021-11-03.
//

#include <iostream>
#include "kitchen.cpp"
#include "orderqueue.cpp"
#include "order.cpp"
#include "dish.cpp"
#include <string>


int main(int argc, const char * argv[]) {
    // Ordering pages Acceptance Tests:
    // 1.After ordering the dishes, make sure the ordered dishes are all added into a order object, and make sure this object is placed at the end of order queue.
    OrderQueue q1;
    std::string dishname1 = "French Fries";
    std::string dishname2 = "Double Cheese Burger";
    std::cout<<"Initialized Dish 1: French Fries, DishID:1 Price:$3.99"<<std::endl;
    Dish dish1(dishname1);
    dish1.setID(1);
    dish1.setprice(3.99);
    std::cout<<"Initialized Dish 2: Double Cheese Burger, DishID:2 Price:$9.99"<<std::endl;
    Dish dish2(dishname2);
    dish2.setID(2);
    dish2.setprice(9.99);
    std::cout<<"Initialized Order OrderID:1 TableID:1"<<std::endl;
    Order order1(1,1,1);
    std::cout<<"Customer added "<<dish1.getname()<<" into Order "<<order1.getorderID()<<std::endl;
    order1.pushItems(dish1);
    std::cout<<"Customer added "<<dish2.getname()<<" into Order "<<order1.getorderID()<<std::endl;
    order1.pushItems(dish2);
    std::cout<<"The order now has dishes:"<<std::endl;
    order1.getItems();
    q1.appendorder(order1);
    // 3.After choosing “Hurry Up!“, the order object with orderID linked to this TableID will be pushed to the head of order queue.
    Order order2(2,1,2);
    Order order3(3,1,3);
    Order order4(4,1,4);
    order2.pushItems(dish2);
    order3.pushItems(dish1);
    q1.appendorder(order2);
    q1.appendorder(order3);
    q1.appendorder(order4);
    std::cout<<"original order queue"<<std::endl;
    q1.displayorders();
    std::cout<<"pushing order 2 to the front"<<std::endl;
    q1.hurry(order2);
    q1.displayorders();
    std::cout<<"pushing order 4 to the front"<<std::endl;
    q1.hurry(order4);
    q1.displayorders();
    // Check if the dishes are arranged according to the order time. If yes, it’ll pass. Otherwise, it fails.
    // Check if the orders are deleted when it completes.
    kitchen k(q1);
    k.viewOrder();
    k.finish();
    k.viewOrder();
}
