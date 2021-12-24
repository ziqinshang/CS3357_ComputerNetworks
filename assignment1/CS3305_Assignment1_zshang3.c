//
//  CS3305_Assignment1_zshang3.c
//  CS3305_lecture2
//
//  Created by David Shang on 2021-09-16.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>


/*

   This program forks a process.  The child and parent processes print to terminal to identify themselves

*/
//wait() forces the parent not to be terminated without the the child process to be finished
int main ()
{
//const char* external_program_path = "../externalprogram/external_program.out";
    pid_t i, j, pid, pid_2, pid_3;
pid=fork();
wait(NULL);
if (pid <0) // fork unsuccessful
 {
    printf("fork unsuccessful");
    exit(1);
 }

if (pid>0) //parent
 {
     wait(NULL);
     pid_2 = fork();
     wait(NULL);
     if (pid_2==0) //child_2
       {
           i = getppid();
           j = getpid();
           //wait(NULL);
           printf("\n parent (PID %d) created child_2 (PID %d)\n", i, j);
//           char string1[20] = "for child_1";
//           char buffer[10];
//           sprintf(buffer, "%d", i);
//           char* msg = strcat(string1, buffer);
//           printf("%s",msg);
           pid_3 = fork();
           wait(NULL);
           if (pid_3==0) //child_2.1
           {
               i = getppid();
               j = getpid();
               printf("\n child_2 (PID %d) created child_2.1 (PID %d)\n", i, j);
               printf("\n child_2.1 (PID %d) is calling an external program external_program.out and leaving child_2\n",j);
               wait(NULL);
               //char string2[20] = "for child_2.1   ";
               char buffer2[10];
               sprintf(buffer2, "%d", j);
               //char* msg2 = strcat(string2, buffer2);
               printf("\n%s\n",buffer2);
               execl("./externalprogram.out","./externalprogram.out", buffer2,NULL);
           }
       }
     printf("\nchild_1 and child_2 are completed and parent process is terminating…\n");
 }

if (pid==0) //child_1
  {
      i = getppid();
      j = getpid();
      printf("\n parent (PID %d) created child_1 (PID %d)\n", i, j);
      printf("\n parent (PID %d) is waiting for child_1 (PID %d) to complete before creating child_2\n", i, j);
      printf("\nchild_1 (PID %d) is calling an external program external_program.out and leaving parent\n",j);
      char string1[20] = "for child_1   ";
      char buffer[10];
      sprintf(buffer, "%d", j);
      char* msg = strcat(string1, buffer);
      //printf("\n%s\n","test");
      execl("./externalprogram.out","./externalprogram.out", msg,NULL);
      //char* msg = strcat(buffer, string1);
      //printf("\n%s\n",msg);
      //char* msg = strcat(i,"for child_1");
      //execl("bin/externalprogram.out",);
  }
    

}
