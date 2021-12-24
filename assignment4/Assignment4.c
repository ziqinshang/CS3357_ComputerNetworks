//
//  main.c
//  CS3305A4
//
//  Created by David Shang on 2021-11-03.
//

#include<stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    // initialzation for the required variables
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    // open the file in given location
    fp = fopen("rr_input.txt", "r");
    // if the file doesnt exit, exit the program
    if (fp == NULL){
        printf("File not found\n");
        exit(EXIT_FAILURE);
        
    }
    int i=0;
    // get every line in the file until there is no more, perform operation for each line
    while ((read = getline(&line, &len, fp)) != -1) {
        //array of input string
        char *char_arr[10];
        int arrival_time[10],burst_time[10],time_quantum;
        printf("Retrieved line of length %zu:\n", read);
        printf("%s", line);
        char *token;
        //use strrchr to get last token of the input string and make it as time quantum
        char *last = strrchr(line, ' ');
        if (last != NULL) {
            char *time_quantumtmp;
            time_quantumtmp = last+1;
            time_quantum = atoi(time_quantumtmp);
            // printf("Last token: '%i'\n", time_quantum);
        }
        // use strtok to retrieve every token and put them into a temporary container
        // j is number of tokens
        int j=0;
        token = strtok(line, " ");
        /* walk through other tokens */
        while( token != NULL ) {
            //printf( " %s\n", token );
            char_arr[j] = token;
            //char_arr[i][j] = token;
            token = strtok(NULL, " ");
            j = j+1;
        }
        // we can know how many processes there is by checking the number of tokens
        // (number of tokens - 1)/3 is the total processes
        int totalprocesses = (j-1)/3;
        // for each process, assign the arrival time and burst time into seperate container
        for(int k=0; k<totalprocesses;k++){
            // the arrival times will be stored at location 1,4,7,10,13.., so (#process*3) + 1
            int tmpatime = atoi(char_arr[(k*3)+1]);
            // the arrival times will be stored at location 2,5,8,11,14.., so (#process*3) + 2
            int tmpbtime = atoi(char_arr[(k*3)+2]);
            // assign the tmptimes into array
            arrival_time[k] = tmpatime;
            burst_time[k] = tmpbtime;
        }
        int count,n,time_elapsed,remain,flag=0;
        int wait_time=0,turnaround_time=0,remaining_time[10];
        n = totalprocesses;
        // number of process remained
        remain=n;
        // at time 0, every process's remaining time is their burst time
        for(count=0;count<n;count++)
        {
            remaining_time[count]=burst_time[count];
        }
        //
        for(time_elapsed=0,count=0;remain!=0;)
        {
            // if a process's remaining time is less than time quantum, we only count the process's remaining time
            if(remaining_time[count]<=time_quantum && remaining_time[count]>0)
            {
                // add the remaining time of the process into total time elapsed
                time_elapsed+=remaining_time[count];
                // then we consider the process is finished and set the finish flag
                remaining_time[count]=0;
                flag=1;
            }
            // if the process's remaining time is greater than time quantum, we dont kill the process and move on
            else if(remaining_time[count]>0)
            {
                // add the time quantum into total time elapsed
                time_elapsed+=time_quantum;
                // deduct the process remaining time
                remaining_time[count]-=time_quantum;
            }
            // if the process is finished, we print it's stats
            if(remaining_time[count]==0 && flag==1)
            {
                remain--;
                printf("Process: P%d Arrival Time: %d Burst time: %d Waiting Time: %d Turnaround Time: %d\n",count+1,arrival_time[count],burst_time[count],time_elapsed-arrival_time[count]-burst_time[count],time_elapsed-arrival_time[count]);
                wait_time += time_elapsed - arrival_time[count] - burst_time[count];
                turnaround_time += time_elapsed - arrival_time[count];
                flag=0;
            }
            if(count==n-1)
                count=0;
            else if(arrival_time[count+1]<=time_elapsed)
                count++;
            else
                count=0;
        }
        printf("Total Turnaround Time = %d",turnaround_time);
        printf("\nAverage Waiting Time= %f\n",wait_time*1.0/n);
        printf("Avg Turnaround Time = %f\n",turnaround_time*1.0/n);
        printf("\n");
        i = i+1;
    }
    
    fclose(fp);
    if (line)
        free(line);
    exit(EXIT_SUCCESS);
}
