// waiter.cpp 
// CS3307Project
//
//  Created by Si Yao on 2021-11-05.

#include "waiter.hpp"
#include "Table.hpp"

using namespace std;

waiter::waiter(int ID, double Tip){
    waiterID = ID;
    inTip = Tip;
}

waiter::~waiter(void){

}

//function: call waiter
//return: the id of called waiter
int waiter::help(int TableID){
    cout << TableID << "is calling..." << endl;
    return waiterID;
}

//a function to get the checkOut value
//return: the tip of table
int waiter::checkOut(int TableID){
    return inTip;
}
