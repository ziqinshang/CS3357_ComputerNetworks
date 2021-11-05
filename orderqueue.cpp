#include <queue>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <orderqueue.h>
#include kitchen.cpp
#include order.cpp
#include table.cpp
using namespace std;

void Orderqueue::add(orderID){
    Orders.push(orderID);
}

void Orderqueue::hurry(orderID){

}

void Orderqueue::finish(orderID){
    
}