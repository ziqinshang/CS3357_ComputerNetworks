//Sha Liu
//This is the order source file, which contains the methods
//2021.11.1

#include "order.h"
using namespace std;
using std::setw;

//A constructor to initialize the attributes of objects of the class when created
//Return a Order type
Order::Order(int oid,int state,int tid){
    orderID=oid;
    orderState=state;
    tableID=tid;
    dishNum=0; // how many dish in this order=一共有多少菜
}

//A destructor to tear things down when objects are destroyed
//return "destruct"
Order::~Order(void){
    // cout<<"destruct"<<endl;
}

//A getter, use it to get order ID
//return order ID
int Order::getorderID(){
    return orderID;
}

//A getter, use it to get order's state
//return order's  state
int Order::getState(){
    return orderState;
}

//A getter, use it to get table ID
//return order's  table ID
int Order::gettableID(){
    return tableID;
}


//print all items' names in order,一个for循环，打印所有点过的菜
void Order::getItems(){
    for ( int i = 0; i < dishNum; i++ ){
        cout << setw( 7 )<< i << setw( 13 ) << orderedItems[ i ]->getname() << endl;
    }
}

std::string Order::getitems_str(){
    std::string items;
    for ( int i = 0; i < dishNum; i++ ){
        items += std::to_string(i) + " : " + orderedItems[ i ]->getname() + "  ";
    }
    return items;
}
//A getter, use it to get the number of ordered dishes
//return order's the number of ordered dishes
int Order::getdishNum(){
    return dishNum;
}

//A setter, use it to set order ID
void Order::setorderID(int i){
    orderID=i;
}

//A setter, use it to set order's state
void Order::setState(int i){
    orderState=i;
}

//A setter, use it to set table ID
void Order::settableID(int i){
    tableID=i;
}

//push dish to ordereditems 把菜加到数组里面
//每次加入新的菜，dishNum+1
void Order::pushItems(Dish dish){
    orderedItems[dishNum]= &dish;
    dishNum+=1;
}

bool Order::ordercompare(Order order1){
    if(orderID == order1.getorderID()){
        return true;
    }
    else return false;
}
