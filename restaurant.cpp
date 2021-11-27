//
//  restaurant.cpp
//  CS3307Project
//
//  Created by David Shang on 2021-11-26.
//

#include "restaurant.hpp"
RestaurantWindow::RestaurantWindow(OrderQueue q,QWidget *parent)
: QMainWindow(parent){
    q1 = q;
    finish_button = new QPushButton("FINISH", this);
    orderqueue_display = new QPlainTextEdit(this);
    needhelp_display = new QLabel(this);
    // set size and location of the button
    finish_button->setGeometry(210,450,200,100);
    // Connect button signal to appropriate slot
    orderqueue_display->setGeometry(10, 50, 400, 400);
    orderqueue_display->setReadOnly(1);
    needhelp_display->setGeometry(420, 50, 400, 200);
    connect(finish_button, &QPushButton::released, this, &::RestaurantWindow::handle_finish_button_pop);
    connect(finish_button, &QPushButton::released, this, &::RestaurantWindow::handle_finish_button_display);
}
void RestaurantWindow::handle_needhelp_button_1(){
    needhelp_display->setText("1");
}
void RestaurantWindow::handle_needhelp_button_2(){
    needhelp_display->setText("2");
}
void RestaurantWindow::handle_needhelp_button_3(){
    needhelp_display->setText("3");
}
void RestaurantWindow::handle_needhelp_button_4(){
    needhelp_display->setText("4");
}
void RestaurantWindow::handle_needhelp_button_5(){
    needhelp_display->setText("5");
}
void RestaurantWindow::handle_needhelp_button_6(){
    needhelp_display->setText("6");
}
void RestaurantWindow::handle_finish_button_pop()
{
    q1.poporder();
}
void RestaurantWindow::handle_finish_button_display()
{
    std::string tmporder = q1.displayorders_str();
    QString orderq = QString::fromStdString(tmporder);
    orderqueue_display->setPlainText(orderq);
}
