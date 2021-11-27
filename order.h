//Sha Liu
//This is the order header file.
//2021.11.1

#ifndef ORDER_H
#define ORDER_H

#include <exception>
#include <new>
#include <typeinfo>
#include <ios>
#include <stdexcept>
#include <iostream>
#include <string>
#include <iomanip>
#include "dish.h"

class Dish;
class Order{

private:
    int orderID;
    int orderState;
    int tableID;
    int dishNum; // how many dish in this order 有多少菜
    Dish* orderedItems[100];//最多点100道菜

public:
    //A constructor
    Order(int,int,int);

    //A destructor
    ~Order();

    //Getters
    int getorderID();
    int getState();
    int gettableID();
    int getdishNum();
    void getItems();//print all items' names in order,打印所有点过的菜
    std::string getitems_str();


    //A setter
    void setorderID(int);
    void setState(int);
    void settableID(int);

    //push dish to ordereditems 把菜加到数组里面
    void pushItems(Dish);
    
    //a function that compare orders
    bool ordercompare(Order);

};

#endif // ORDER_H
