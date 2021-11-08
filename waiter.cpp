// waiter.cpp 
// CS3307Project
//
//  Created by Si Yao on 2021-11-05.

#include "waiter.h"
#include "Table.h"

using namespace std;

Waiter::Waiter(int ID, double Tip){
    waiterID = ID;
    inTip = Tip;
}

Waiter::~Waiter(void){

}

//function: call waiter
//return: the id of called waiter
int Waiter::help(int TableID){
    cout << "Table "<<TableID << " is calling waiter " <<waiterID<< endl;
    return waiterID;
}

//a function to get the checkOut value
//return: the tip of table
int Waiter::checkOut(int TableID){
    return inTip;
}
