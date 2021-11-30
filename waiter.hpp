//  waiter.hpp
//  CS3307Project
//
//  Created by Si Yao on 2021-11-05.
//

#ifndef waiter_hpp
#define waiter_hpp

#include <stdio.h>

class waiter{
private:
    int waiterID;
    double inTip;
public:
    waiter(int, double);
    ~waiter();
    int help(int);
    int checkOut(int);
};

#endif