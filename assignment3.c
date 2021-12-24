#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <string.h>
int sumresult = 0;
int port[2];
void *sum(void *thread_id)
{
    char *tmp[20];
    char *xtmp;
    char *ytmp;
    const char s[2] = ",";
    read(port[0],tmp, 50);
    xtmp = strtok(tmp, s);
    ytmp = strtok(NULL,s);
    int x = atoi(xtmp);
    int y = atoi(ytmp);
    int *id = (int*)thread_id;
    printf("thread (TID %d) reads X = %d and Y = %d from the pipe\n", *id, x, y);
    int result = x+y;
    printf("thread (TID %d) writes X + Y = %d to the pipe\n", *id,result);
    sprintf(tmp, "%d", result);
    write(port[1], tmp, 50);
    return 0;
}
void *odd_even(void *thread_id){
    int tmp = 0;
    char *tmpstr[20];
    read(port[0],tmpstr, 50);
    tmp = atoi(tmpstr);
    int *id = (int*)thread_id;
    printf("thread (TID %d) reads X + Y = %d from the pipe\n", *id,tmp);
    if (tmp%2 == 0){
        printf("thread (TID %d) identifies X + Y = %d as an even number\n", *id,tmp);
    }
    else printf("thread (TID %d) identifies X + Y = %d as an odd number\n", *id,tmp);
    printf("thread (TID %d) writes X + Y = %d to the pipe\n", *id,tmp);
    sprintf(tmpstr, "%d", tmp);
    write(port[1], tmpstr, 50);
    return 0;
}
void *digit_count(void *thread_id){
    int tmp = 0;
    char *tmpstr[20];
    read(port[0],tmpstr, 50);
    tmp = atoi(tmpstr);
    int *id = (int*)thread_id;
    printf("thread (TID %d) reads X + Y = %d from the pipe\n", *id,tmp);
    int length = 0;
    long temp = 1;
    while (temp <= tmp) {
        length++;
        temp *= 10;
    }
    printf("thread (TID %d) identifies X + Y = %d as an %d digits number\n", *id,tmp,length);
    return 0;
}
int main(int argc, char** argv)
{
    char *xchar = argv[1];
    char *ychar = argv[2];
    char *tmpchar[20];
    strcpy(tmpchar, ychar);
    int x = atoi(xchar);
    int y = atoi(ychar);
    printf("Parent (PID %d) reads X = %d and Y = %d from the user\n", getpid(), x, y);
    strcat(xchar, ",");
    strcat(xchar, tmpchar);
    if (pipe(port) < 0){
      perror("pipe error");
      exit(0);
    }
    printf("Parent (PID %d) writes X = %d and Y = %d to the pipe\n", getpid(), x, y);
    write(port[1], xchar, 50);
    int i = 100, j = 101, k = 102;

    pthread_t thread_1,thread_2,thread_3;
    
    pthread_create(&thread_1, NULL, sum, &i);
    pthread_create(&thread_2, NULL, odd_even, &j);
    pthread_create(&thread_3, NULL, digit_count, &k);
    pthread_join(thread_1, NULL);
    pthread_join(thread_2, NULL);
    pthread_join(thread_3, NULL);

    printf("All threads terminated...\n");
    
return 0;

}
