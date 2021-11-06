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

class kitchen{
public:
    kitchen();
    ~kitchen();
    void viewOrder(std::queue<Order>);
    bool finish(int);
};

#endif
