//
//  restaurant.hpp
//  CS3307Project
//
//  Created by David Shang on 2021-11-26.
//

#ifndef restaurant_hpp
#define restaurant_hpp

#include <stdio.h>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QPlainTextEdit>
#include <QtWidgets/QLabel>
#include "orderqueue.h"
#include "order.h"
#include "Table.hpp"
namespace Ui {
  class RestaurantWindow;
}
class RestaurantWindow: public QMainWindow
{
  Q_OBJECT
public:
  explicit RestaurantWindow(OrderQueue q, QWidget *parent = nullptr);
    void handle_needhelp_button_1();
    void handle_needhelp_button_2();
    void handle_needhelp_button_3();
    void handle_needhelp_button_4();
    void handle_needhelp_button_5();
    void handle_needhelp_button_6();
private slots:
    void handle_finish_button_pop();
    void handle_finish_button_display();
private:
    OrderQueue q1;
    QPushButton *finish_button;
    QPlainTextEdit *orderqueue_display;
    QLabel *needhelp_display;
};
#endif /* restaurant_hpp */
