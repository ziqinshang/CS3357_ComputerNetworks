//
//  Table.cpp
//  CS3307Project
//
//  Created by David Shang on 2021-11-03.
//

#include "Table.h"
using namespace std;
Table::Table(int id,int state,double price){
    tableID = id;
    tablestate = state;
    tableprice = price;
}
Table::~Table(void){
    
}
//initialize and return a empty order, this order is under this specific table
Order Table::neworder(int ordernum){
    Order tmporder(ordernum,1,tableID);
    return tmporder;
}
void Table::needhelp(){
    cout<<"Table"<<tableID<<" needs help now!"<<endl;
}
void Table::tips(int waiterid, double tip){
    //to be implemented later, need waiter class
    cout<<"tip: $"<<tip<<endl;
    tableprice += tip;
}
double Table::checkout(){
    return tableprice;
}
void Table::rate(Dish a,int r){
    a.updaterate(r);
}
