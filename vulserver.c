#include<stdio.h>
#include<string.h>
#include <Winsock2.h>
#pragma comment(lib, "ws2_32.lib") //Winsock Library

//Vulnerable Function using strcpy
int vulnerable_function(char *input)
{
	char buffer[128];
	strcpy(buffer,input);
	return 1;
}

//Main Function
int main()
{
	WSADATA wsa;
	SOCKET master , new_socket;
	struct sockaddr_in server, address;
	int addrlen, valread;

	//Size of the receive buffer
	char *buffer;
	buffer = (char*) malloc((1024 + 1) * sizeof(char));
	WSAStartup(MAKEWORD(2,2),&wsa);

	//Create a socket
	master = socket(AF_INET , SOCK_STREAM , 0 );
	printf("Socket created.\n");

	//Prepare the sockaddr_in structure
	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY;
	server.sin_port = htons( 10000 );

	//Bind
	bind(master ,(struct sockaddr *)&server , sizeof(server));

	//Listen for incoming connections
	listen(master , 1);

	//Accept the incoming connection
	puts("Waiting for incoming connections…");
	addrlen = sizeof(struct sockaddr_in);
	new_socket = accept(master , (struct sockaddr *)&address, (int *)&addrlen);
	printf("New connection , socket fd is %d , ip is : %s , port : %d \n" , new_socket , inet_ntoa(address.sin_addr) , ntohs(address.sin_port));

	valread = 1;
	//Receiving Loop
	while(valread != 0)
	{
		valread = recv(new_socket, buffer, 1024, 0);
		if ( valread == 2) //Server close the connection when a return is send from the client
		{
		closesocket( new_socket );
		exit(0);
		}
		buffer[valread]=" ";
		vulnerable_function(buffer);
		printf("%s:%d – %s \n" , inet_ntoa(address.sin_addr) , ntohs(address.sin_port), buffer);
		send( new_socket , buffer , valread , 0 );
	}
	closesocket(new_socket);
	WSACleanup();
	return 0;
}
