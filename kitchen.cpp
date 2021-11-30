<<<<<<< HEAD
// kitchen.cpp
//  CS3307Project
//
//  Created by Si Yao on 2021-11-05.
#include <stdio.h>
#include "kitchen.hpp"

using namespace std;

kitchen::kitchen(OrderQueue queue){
    q=queue;
}

kitchen::~kitchen(void){
    //cout<<"destruct kitchen class"<<endl;
}

//A viewer, use it to view the order in orderqueue
// no return
void kitchen::viewOrder(){
    q.displayorders();
}

//A finisher, use it to note the orderID is finished
// return bool value
void kitchen::finish(){
    q.poporder();
}
=======
// kitchen.cpp
//  CS3307Project
//
//  Created by Si Yao on 2021-11-05.
#include <stdio.h>
#include "kitchen.h"

using namespace std;

kitchen::kitchen(OrderQueue queue){
    q=queue;
}

kitchen::~kitchen(void){
    //cout<<"destruct kitchen class"<<endl;
}

//A viewer, use it to view the order in orderqueue
// no return
void kitchen::viewOrder(){
    q.displayorders();
}

//A finisher, use it to note the orderID is finished
// return bool value
void kitchen::finish(){
    q.poporder();
}
>>>>>>> 5950259a50b12d9c0a239bd8591082712a3fe0dc
