#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

void syscmd(char * command, char result[]){
	FILE* fp = popen(command, "r");
	if (!fp)
		printf("[!] Unable to run command\n");
	fscanf(fp,"%s",result);
	pclose(fp);
}

int get_pid(char const *name){
	char result[100];
	// build the command 
	char * cmd = (char *)malloc(25*sizeof(char));
	sprintf(cmd,"pidof %s", name);
	// run the command 
	syscmd(cmd, result);
	// free the command 
	free(cmd);
	// return converted result 
	return atoi(result);
}

void findHeap(int pid, char *result){
	char * cmd = (char*)malloc(46*sizeof(char));
	sprintf(cmd, "cat /proc/%d/maps | grep [heap]",pid);
	syscmd(cmd,result);
	printf("%s\n", result);
	free(cmd);
}

void attach(int pid){
	ptrace(PTRACE_ATTACH, pid, NULL, NULL);
	waitpid(pid, NULL, 0);
}

void detach(int pid){
	ptrace(PTRACE_DETACH, pid, NULL, NULL);
}


