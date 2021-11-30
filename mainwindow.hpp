//
//  mainwindow.hpp
//  CS3307Project
//
//  Created by David Shang on 2021-11-26.
//

#ifndef mainwindow_hpp
#define mainwindow_hpp

#include <stdio.h>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include "orderqueue.h"
#include "order.h"
namespace Ui {
  class MainWindow;
}
class MainWindow : public QMainWindow
{
  Q_OBJECT
public:
  explicit MainWindow(OrderQueue q, QWidget *parent = nullptr);
private slots:
    void handle_hurry_button_1();
    void handle_hurry_button_2();
    void handle_hurry_button_3();
    void handle_hurry_button_4();
    void handle_hurry_button_5();
    void handle_hurry_button_6();
private:
    OrderQueue q1;
    QPushButton *hurry_button;
    QPushButton *needhelp_button;
};
#endif /* mainwindow_hpp */
