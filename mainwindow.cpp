//
//  mainwindow.cpp
//  CS3307Project
//
//  Created by David Shang on 2021-11-26.
//

#include "mainwindow.hpp"
#include "restaurant.hpp"
MainWindow::MainWindow(OrderQueue q, QWidget *parent)
  : QMainWindow(parent)
{
    RestaurantWindow restaurant(q);
    q1 = q;
  // Create the button, make "this" the parent
  hurry_button = new QPushButton("HURRY", this);
  // set size and location of the button
  hurry_button->setGeometry(210,450,200,100);
    needhelp_button = new QPushButton("NEEDHELP", this);
    needhelp_button->setGeometry(600,450,50,50);
  // Connect button signal to appropriate slot
    connect(hurry_button, &QPushButton::released, this, &::MainWindow::handle_hurry_button_1);
    // connect(hurry_button, &QPushButton::released, this, &::MainWindow::handle_hurry_button_1);
}

void MainWindow::handle_hurry_button_1()
{
    q1.hurry(q1.findorderbytableid(1));
}
void MainWindow::handle_hurry_button_2()
{
    q1.hurry(q1.findorderbytableid(2));
}
void MainWindow::handle_hurry_button_3()
{
    q1.hurry(q1.findorderbytableid(3));
}
void MainWindow::handle_hurry_button_4()
{
    q1.hurry(q1.findorderbytableid(4));
}
void MainWindow::handle_hurry_button_5()
{
    q1.hurry(q1.findorderbytableid(5));
}
void MainWindow::handle_hurry_button_6()
{
    q1.hurry(q1.findorderbytableid(6));
}
