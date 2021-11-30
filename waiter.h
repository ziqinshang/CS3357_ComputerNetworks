//  waiter.hpp
//  CS3307Project
//
//  Created by Si Yao on 2021-11-05.
//

#ifndef waiter_h
#define waiter_h

#include <stdio.h>

class Waiter
{
    private:
        int waiterID;
        double inTip;
    public:
        Waiter(int, double);
        ~Waiter();
        int help(int);
        int checkOut(int);
};

#endif