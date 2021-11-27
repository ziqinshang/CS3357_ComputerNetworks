//Sha Liu
//This is the dish source file, which contains the methods
//2021.11.1

#include "dish.h"
using namespace std;

//A constructor to initialize the attributes of objects of the class when created
//Return a Dish type
Dish::Dish(std::string input){
    name=input;
    pic="";
    price=0; // Dish's price
    dishID=0; //Dish's ID
    totalRate=0; // Total of all ratings
    totalServed=0; // The total number of times the dish was rate
    rate=0;
}

//A destructor to tear things down when objects are destroyed
//return "destruct"
Dish::~Dish(void){
    // cout<<"destruct"<<endl;
}

//A getter, use it to get name of dish
//return dish's name
std::string Dish::getname(){
    return name;
}

//A getter, use it to get name of dish's picture
//return name of dish's picture
std::string Dish::getpic(){
    return pic;
}

//A getter, use it to get name of dish's picture
//return name of dish's picture
double Dish::getprice(){
    return price;
}

//A getter, use it to get dish's ID
//return dish's ID
int Dish::getID(){
    return dishID;
}

//A getter, use it to get dish's total rating
//return dish's total rating
int Dish::getTotalR(){
    return totalRate;
}

//A getter, use it to get the dish's rating times
//return  dish's rating times
int Dish::getTotalS(){
    return totalServed;
}

//A getter, use it to get the dish's rate
//return dish's rate
int Dish::getrate(){
    return rate;
}

//A setter, use it to set dish's name
void Dish::setname(std::string i){
    name=i;
}

//A setter, use it to set name of dish's picture
void Dish::setpic(std::string i){
    pic=i;
}

//A setter, use it to set dish's price
void Dish::setprice(double i){
    price=i;
}

//A setter, use it to set dish's ID
void Dish::setID(int i){
    dishID=i;
}

//A setter, use it to set dish's total rate
void Dish::setTotalR(int i){
    totalRate=i;
}

//A setter, use it to set total rating times of the dish
void Dish::setTotalS(int i){
    totalServed=i;
}

//A setter, use it to set dish's average rate
void Dish::setrate(int i){
    rate=i;
}

//A setter, use it to set dish's average rate
void Dish::updaterate(int i){
    totalServed++;
    totalRate = totalRate + i;
}

//A method to calculate average rate of the dish
//return the average rate of this dish, and it can return -1 in some case
int Dish::averageRate(){
    if (totalRate==0||totalServed==0){
        cout<<"No one scored this dish"<<endl;
        return -1;
    }
    else {
        rate=totalRate/totalServed;
        return rate;
    }
}
