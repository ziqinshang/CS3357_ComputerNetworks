#include<stdio.h>
#include<string.h>
#include<pthread.h>
#include<stdlib.h>
#include<unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define withdraw_req 400
#define NUM_THREADS 5


void  *withdraw_money(void *thread_id);
void  *deposit_money(void *thread_id);
//global variables
int shared_balance = 1000;
int numofaccounts = 0;
int numofclients = 0;
int account_balances[10];
char* client_op[10];
char *client_operations[10][50];
pthread_mutex_t lock;

//the thread function
void *process(void *arg){
    //printf("\nhello");
    //printf( " %s\n", arg);
    //process customer operation first
    char *newline = (char *) arg;
    //printf( " %s\n", newline );
    char *char_arr[50];
    char *token;
    int j=0;
    token = strtok(newline, " ");
    /* walk through other tokens */
    while( token != NULL ) {
        char_arr[j] = token;
        //printf( " %s\n", token );
        token = strtok(NULL, " ");
        j = j+1;
    }
    int totalprocesses = (j-1)/3;
    for(int k=0; k<totalprocesses;k++){
        char *transcation_type = char_arr[(k*3)+1];
        if(strcmp(transcation_type, "w")==0){
            char *whichaccount = char_arr[(k*3)+2];
            int accountnumber = (int) (whichaccount[1] - '0');
            int transcation_amount = atoi(char_arr[(k*3)+3]);
            pthread_mutex_lock(&lock);  // ENTRY
            /*****CRITICAL SECTION STARTS ******/
            if(account_balances[accountnumber-1]>=transcation_amount){
                printf("\n successfully withdrawed $%d for account #a%d", transcation_amount,accountnumber);
                account_balances[accountnumber-1] = account_balances[accountnumber-1] - transcation_amount;
                printf("\n updated balance: $%d for account #a%d", account_balances[accountnumber-1],accountnumber);
            }
            else{
                printf("\n Request denied of $%d for account #a%d", transcation_amount,accountnumber);
                printf("\n balance: $%d for account #a%d", account_balances[accountnumber-1],accountnumber);
            }
            /***** CRITICAL SECTION ENDS ******/
            pthread_mutex_unlock(&lock); // EXIT
        }
        else if(strcmp(transcation_type, "d")==0){
            char *whichaccount = char_arr[(k*3)+2];
            int accountnumber = (int) (whichaccount[1] - '0');
            int transcation_amount = atoi(char_arr[(k*3)+3]);
            pthread_mutex_lock(&lock);  // ENTRY
            /*****CRITICAL SECTION STARTS ******/
            account_balances[accountnumber-1] = account_balances[accountnumber-1] + transcation_amount;
            printf("\n successfully deposited $%d for account #a%d", transcation_amount,accountnumber);
            printf("\n updated balance: $%d for account #a%d", account_balances[accountnumber-1],accountnumber);
            /***** CRITICAL SECTION ENDS ******/
            pthread_mutex_unlock(&lock); // EXIT
        }
    }
    return 0;
}

int main(void)
{
FILE * fp;
char * line = NULL;
size_t len = 0;
ssize_t read;
// open the file in given location
fp = fopen("assignment_6_input.txt", "r");
// if the file doesnt exit, exit the program
if (fp == NULL){
    printf("File not found\n");
    exit(EXIT_FAILURE);
}
while ((read = getline(&line, &len, fp)) != -1) {
    int j=0;
    char *token;
    char tmpline[100];
    strcpy(tmpline, line);
    char *char_arr[50];
    token = strtok(line, " ");
    /* walk through other tokens */
    while( token != NULL ) {
        char_arr[j] = token;
        token = strtok(NULL, " ");
        j = j+1;
    }
    if(j==3 && (strcmp(char_arr[1], "b")==0)){
        account_balances[numofaccounts] = atoi(char_arr[2]);
        numofaccounts++;
    }
    if(j>3){
        client_op[numofclients]=malloc(sizeof(tmpline));
        strcpy(client_op[numofclients], tmpline);
        numofclients++;
    }
}
//for(int i=0;i<numofaccounts;i++){
//    printf("%i\n",account_balances[i]);
//}
//for(int i=0;i<numofclients;i++){
//    printf("%s\n",client_op[i]);
//}
    
int i, err_thread;

pthread_t threads[numofclients];

if (pthread_mutex_init(&lock, NULL) != 0)
    {
        printf("\n mutex init failed\n");
        return 1;
    }


for (i = 0; i< numofclients; i++)
  {
    err_thread = pthread_create(&threads[i], NULL, &process, client_op[i]);
if (err_thread != 0)
    printf("\n Error creating thread %d", i);
}


for (i = 0; i< numofclients; i++)
    pthread_join(threads[i], NULL);
    printf("\n");
for(int i=0;i<numofaccounts;i++){
        printf("a%i b %i\n",i+1,account_balances[i]);
}


pthread_mutex_destroy(&lock);

return 0;

}
