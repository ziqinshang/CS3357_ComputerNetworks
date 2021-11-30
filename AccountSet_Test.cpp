/**
 * This is the test for User story "Account setting"
 * 
 */

#include <iostream>
#include "dish.cpp"
#include "order.cpp"
#include "Table.cpp"
#include "waiter.cpp"
using namespace std;

int main(int argc, const char * argv[]) {
    // insert code here...
    int tableId=1, tableState=0, waiterId=24;
    double price=0, tip=0;
    string ans;
    Table table(tableId, tableState, price);
    Waiter waiter(waiterId, tip);
    cout<<"Your table Id is 1"<<endl;
    cout<<"waiter "<<waiterId<<" will serve you"<<endl;
    cout<<"Do you need help now?(y/n)"<<endl;
    cin>>ans;
    if(ans == "y"){
        table.needhelp();
        waiter.help(tableId);
    }else{
        cout<<"Please take your time"<<endl;
    }
    
    //cout << "Hello, World!\n";
    return 0;
}
