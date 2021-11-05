// kitchen.cpp
//  CS3307Project
//
//  Created by Si Yao on 2021-11-05.
#include <stdio.h>
#include "kitchen.hpp"

using namespace std;

kitchen::kitchen(){

}

kitchen::~kitchen(void){
    cout<<"destruct kitchen class"<<endl;
}

//A viewer, use it to view the order in orderqueue
// no return
void kitchen::viewOrder(queue<Order> orderqueue){
    // only the front element of queue is available
    int queueSize = orderqueue.size();
    for(int i=0; i<queueSize; i++){
        cout << setw( 7 )<< orderqueue.front().getorderID() << setw( 13 ) << endl;
        orderqueue.push(orderqueue.front());
        orderqueue.pop();
    }
}

//A finisher, use it to note the orderID is finished
// return bool value
bool finish(int orderID){
    return true;
}