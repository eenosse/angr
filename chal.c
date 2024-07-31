#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned char command[3000];
int cmd_ptr = 0;
unsigned char input[300];
int inp_ptr = 0;

int read_command(const char *a1)
{
    FILE *stream = fopen(a1, "rb"); // Open the file in binary mode

    if (stream)
    {
        fseek(stream, 0, SEEK_END); // Move the file pointer to the end
        long file_size = ftell(stream); // Get the file size
        fseek(stream, 0, SEEK_SET); // Reset the file pointer to the beginning

        if (file_size > 3000)
        {
            puts("Code too large!");
            fclose(stream);
            return 1;
        }

        fread(command, 1, file_size, stream); // Read the entire file into 'command'
        fclose(stream);
        return 0;
    }
    else
    {
        printf("No file named %s\n", a1);
        return 1;
    }
}

int input_char(unsigned char c) {
    input[inp_ptr++] = c;
    return 0LL;
}

unsigned char sub_1315()
{
    return input[--inp_ptr];
}

int process_code()
{
    unsigned char v1; // al
    char opcode; // [rsp+Fh] [rbp-11h]
    unsigned char mem[8]; // [rsp+10h] [rbp-10h]

    // (unsigned long long*)mem[0] = 0LL;
    while ( 1 )
    {
        opcode = command[cmd_ptr++];
        if ( opcode == 13 )
        {
            break;
        }

        switch ( opcode )
        {
            case '>':
                putchar((unsigned char)command[cmd_ptr]);
                ++cmd_ptr;
                break;

            case '?':
                v1 = getchar();
                input_char(v1);
                break;

            case ',':
                mem[command[cmd_ptr]] = command[cmd_ptr + 1];
                cmd_ptr += 2;
                break;

            // case '.':
            //     mem[command[cmd_ptr]] = *((_BYTE *)mem
            //                                                           + (unsigned __int8)command[cmd_ptr + 1]);
            //     cmd_ptr += 2;
            //     break;

            case '!':
                mem[command[cmd_ptr]] = mem[command[cmd_ptr+1]] + mem[command[cmd_ptr+2]];
                cmd_ptr += 3;
                break;

            case '|':
                mem[command[cmd_ptr]] = mem[command[cmd_ptr+1]] - mem[command[cmd_ptr+2]];
                cmd_ptr += 3;
                break;

            case '@':
                mem[command[cmd_ptr]] = mem[command[cmd_ptr+1]] ^ mem[command[cmd_ptr+2]];
                cmd_ptr += 3;
                break;

            case '$':
                mem[0] = sub_1315();
                break;

            case '=':
                // sub_12DC(*((_BYTE *)mem + (unsigned __int8)command[cmd_ptr]));
                if (mem[7] != command[cmd_ptr]) {
                    printf("Nope!");
                    exit(1);
                }
                ++cmd_ptr;
                break;
        }
    }

    return 0;
}

int main(int argc, char **argv, char **env){
    if ( argc == 2 )
    {
        if ( (unsigned int)read_command(argv[1]) == 1 )
        {
            return 0LL;
        }
        else
        {
            if ( process_code() )
            {
                puts("Nope!");
            }
            else
            {
                puts("Correct!!!");
            }

            return 0LL;
        }
    }
    else
    {
        puts("Usage: ./chal command_file");
        return 0LL;
    }
}