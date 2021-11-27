//
//  kitchen.hpp
//  CS3307Project
//
//  Created by Si Yao on 2021-11-05.

#ifndef waiter_hpp
#define waiter_hpp

#include <stdio.h>
#include <queue>
#include "order.h"
#include "orderqueue.h"
class kitchen{
private:
    OrderQueue q;
public:
    kitchen(OrderQueue);
    ~kitchen();
    void viewOrder();
    void finish();
};

#endif
