#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

int main(int argc, char** argv){
    int n;
    int status;
    char c;
    char x[20],y[20],z[20];
    int port[2];
    pid_t pid;
    char *x1 = argv[1];
    char *y1 = argv[2];
    char *z1 = argv[3];
    strcpy(x, x1);
    strcpy(y, y1);
    strcpy(z, z1);
//    printf("\n From parent: Please input X\n");
//    scanf("%s",x);
//    printf("\n From Child: Please input Y\n");
//      scanf("%s",y);
//    printf("\n From Child: Please input Z\n");
//      scanf("%s",z);
 
  if (pipe(port) < 0){
    perror("pipe error");
    exit(0);
  }

  pid = fork();
    
  if (pid < 0) {
    perror("fork error");
    exit(0);
  }

  if(pid > 0) //parent
  {
      printf("\n parent (PID %d) created a child (PID %d)\n",getpid(),getppid());
//      printf("\n From parent: Please enter X\n");
//      scanf("%s",x);
      printf("\nparent (PID %d) receives X = %s from the user\n",getpid(),x);
      write(port[1],x, 50);
      printf("\nparent (PID %d) writes X = %s to the pipe\n",getpid(),x);
      printf("\n From parent: waiting for child to complete..\n");
      wait(NULL);
      read (port[0],x,50);
      printf("\nparent (PID %d) reads concatenated result from the pipe (Z' = %s)\n", getpid(),x);
  }
  
  if(pid==0) //child
   
  {

      printf("\n child (PID %d) receives Y = %s and Z = %s from the user \n",getpid(),y,z);
      strcat(y, z);
      printf("\n child (PID %d) concatenates Y and Z to generate Y' = %s \n",getpid(),y);
    read (port[0],x,50);
    printf("\n child (PID %d) reads X from pipe = %s\n", getpid(),x);
      strcat(x, y);
      printf("\n child (PID %d) concatenates s X and Y' to generate Z' = %s \n",getpid(),x);
      printf("\nchild (PID %d) writes Z' into the pipe\n",getpid());
      write(port[1],x, 50);


  }

  return 0;

}
