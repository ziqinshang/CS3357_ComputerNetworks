#include <queue>
#include <iostream>
#include <string>
#include <stdlib.h>
#include "orderqueue.h"
#include "kitchen.h"
#include "order.h"
#include "Table.h"
using namespace std;
int OrderQueue::getsize(){
    return orderqueue.size();
}
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
