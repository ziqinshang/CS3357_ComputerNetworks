#include <queue>
#include <iostream>
#include <string>
#include <stdlib.h>
#include "orderqueue.h"
<<<<<<< HEAD
#include "kitchen.hpp"
#include "order.h"
#include "Table.hpp"
=======
#include "kitchen.h"
#include "order.h"
#include "Table.h"
>>>>>>> 5950259a50b12d9c0a239bd8591082712a3fe0dc
using namespace std;
int OrderQueue::getsize(){
    return orderqueue.size();
}
<<<<<<< HEAD
std::string OrderQueue::displayorders_str(){
    std::string orders_str;
    int queueSize = orderqueue.size();
    for(int i=0; i<queueSize; i++){
        std::string current_str;
        current_str = "TableID: " + std::to_string(orderqueue.front().gettableID());
        current_str += " OrderID: " + std::to_string(orderqueue.front().getorderID());
        current_str += "\n";
        current_str += "Items: " + orderqueue.front().getitems_str();
        current_str += "\n";
        orders_str.append(current_str);
        orderqueue.push(orderqueue.front());
        orderqueue.pop();
    }
    return orders_str;
}
=======
>>>>>>> 5950259a50b12d9c0a239bd8591082712a3fe0dc
void OrderQueue::displayorders(){
    int queueSize = orderqueue.size();
    for(int i=0; i<queueSize; i++){
        cout << orderqueue.front().getorderID()<< "->";
        orderqueue.push(orderqueue.front());
        orderqueue.pop();
    }
    cout<<endl;
}
void OrderQueue::appendorder(Order neworder){
    orderqueue.push(neworder);
}
void OrderQueue::poporder(){
    orderqueue.pop();
}
void OrderQueue::hurry(Order priorityorder){
    int queueSize = orderqueue.size();
    std::queue<Order> neworderqueue;
    neworderqueue.push(priorityorder);
    for(int i=0; i<queueSize; i++){
        if (priorityorder.ordercompare(orderqueue.front())) {
            orderqueue.pop();
            continue;
        }
        neworderqueue.push(orderqueue.front());
        orderqueue.pop();
    }
    orderqueue = neworderqueue;
}
<<<<<<< HEAD
Order OrderQueue::findorderbytableid(int tableid){
    int queueSize = orderqueue.size();
    std::queue<Order> neworderqueue;
    for(int i=0; i<queueSize; i++){
        orderqueue.push(orderqueue.front());
        neworderqueue.push(orderqueue.front());
        orderqueue.pop();
    }
    for(int i=0; i<queueSize; i++){
        if (neworderqueue.front().gettableID()==tableid) {
            return neworderqueue.front();
        }
    }
    return Order(-1, -1, -1);
}
//void OrderQueue::hurrybytableid(int tableid){
//    int queueSize = orderqueue.size();
//    std::queue<Order> neworderqueue;
//    std::queue<Order> neworderqueue2;
//    for(int i=0; i<queueSize; i++){
//        if (orderqueue.front().gettableID()==tableid) {
//            neworderqueue2.front() = orderqueue.pop();
//            continue;
//        }
//        neworderqueue.push(orderqueue.front());
//        orderqueue.pop();
//    }
//    orderqueue = neworderqueue;
//}
=======
>>>>>>> 5950259a50b12d9c0a239bd8591082712a3fe0dc
//void Orderqueue::add(orderID){
//    Orders.push(orderID);
//}
//
//void Orderqueue::hurry(orderID){
//
//}
//
//void Orderqueue::finish(orderID){
//
//}
