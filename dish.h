//Sha Liu
//This is the dish header file.
//2021.11.1

#ifndef DISH_H
#define DISH_H

#include <exception>
#include <new>
#include <typeinfo>
#include <ios>
#include <stdexcept>
#include <iostream>
#include <string>

class Dish{

private:
    std::string pic; // Dish's jpg file name
    std::string name; // Dish's name
    double price; // Dish's price
    int dishID; //Dish's ID
    int totalRate; // Total of all ratings, 所有评分加在一起的数
    int totalServed; // The total number of times the dish was rate, 评分的次数
    int rate; // Average rate of this dish, 这道菜的平均分

public:
    //A constructor
    Dish(std::string);

    //A destructor
    ~Dish();

    //Getters
    std::string getname();
    std::string getpic();
    //Dish getdishbyid(int);
    double getprice();
    int getID();
    int getTotalR();
    int getTotalS();
    int getrate();

    //A setter
    void setname(std::string);
    void setpic(std::string);
    void setprice(double);
    void setID(int);
    void setTotalR(int); //set total rate
    void setTotalS(int); //set total times of rate
    void setrate(int);
    void updaterate(int);

    //Calculate average rate
    int averageRate();
};

#endif // DISH_H
