#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <ctype.h>
#include <arpa/inet.h>
#include <unistd.h>

typedef short int16_t;


int main(int argc, char const *argv[])
{
	int l = 3;
	char const *host;
	int sock, err;
	int fromPort = atol(argv[2]);
	int toPort = atol(argv[3]);
	struct sockaddr_in sockAddr;
	int openPort[toPort - fromPort];
	int openPortIndex = 0;
	
	host = malloc(sizeof(char) * l);
	host = argv[1];
	printf("Scanning %s from Port %d to Port %d...\n", host, fromPort, toPort);
	

	if(isdigit(host[0]))
    {
        sockAddr.sin_addr.s_addr = inet_addr(host);
    }
	strncpy((char*)&sockAddr , "" , sizeof sockAddr);
	sockAddr.sin_family = AF_INET;
	sockAddr.sin_addr.s_addr = inet_addr(host);
	for (int i = fromPort; i < toPort + 1; ++i)
	{
		printf("-Testing %d\n", i);
		sockAddr.sin_port = htons(i); //Htons convert the int i in a type accepted by sockAddr struct.
		sock = socket(AF_INET, SOCK_STREAM, 0);
		if(sock < 0) 
        {
            exit(1);
        }

        err = connect(sock , (struct sockaddr*)&sockAddr , sizeof sockAddr);
         
        if(err < 0)
        {
            fflush(stdout);
        }
        else
        {
            printf("%d open\n",  i);
            openPort[openPortIndex] = i;
            openPortIndex++;
        }
        close(sock);
	}	
	printf("\nScan Finished !\n");
	
	if (openPortIndex > 0)
	{
		for (int i = 0; i < openPortIndex; ++i)
		{
			printf("%d\n", openPort[i]);
		}
	}
	else
	{
		printf("No port opened on range %d-%d\n", fromPort, toPort);
	}
	return 0;
}