//
//  Table.hpp
//  CS3307Project
//
//  Created by David Shang on 2021-11-03.
//

#ifndef Table_hpp
#define Table_hpp

#include <stdio.h>
#include "dish.h"
#include "order.h"

class Table{
private:
    int tableID;
    int tablestate;
    double tableprice;
public:
    Table(int,int,double);
    ~Table();
    Order neworder(int);
    void needhelp();
    void hurry(int);
    void tips(int,double);
    double checkout();
    void rate(Dish ,int);
};
#endif /* Table_hpp */
