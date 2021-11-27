/**
 * This is the acceptance test for User story "tipping system"
 */

#include <iostream>
#include "Table.cpp"
#include "waiter.cpp"
#include "dish.cpp"
#include "order.cpp"
using namespace std;

int main(int argc, const char * argv[]){
    int orderPrice=60;
    string ans;
    string tip_type;
    int percentage, amount, tip;
    Table table(1,0,orderPrice);
    int waiterId = 24;
    cout<<"------Checking out------"<<endl;
    cout<<"The amount of order is $"<<orderPrice<<endl;
    cout<<"Would you like to give some tips to the server?(y/n)"<<endl;
    cin>>ans;
    if(ans == "y"){
        cout<<"what kind of amount you want to give?(%/$)"<<endl;
        cin>>tip_type;
        if(tip_type == "%"){
            cout<<"How many Percentage?"<<endl;
            cin>>percentage;
            if(percentage<100 && percentage>0)
                tip=orderPrice*percentage/100;
            else{
                cout<<"Error!"<<endl;
                return 0;
            }
                
            
        }
        else if(tip_type == "$"){
            cout<<"What Amount?"<<endl;
            cin>>amount;
            tip=amount;

        }
        
        table.tips(waiterId, tip);
    }
    else{
        cout<<"Thank you! Have a good day!"<<endl;
    }
    return 0;
}