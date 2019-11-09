#include <stdio.h>
#include <unistd.h>

static const char* filename = "words.txt";

int main()
{
    FILE* f = NULL;
    char buf[512] = {0};
    int error = 0;

    if (access(filename, F_OK) == 0 && access(filename, R_OK) != 0)
    {
        puts("Hey, don't put words in my mouth!");
        return 1;
    }

    puts("Hi, I'm your friendly neighborhood parrot! Here's what I have to say:");
    f = fopen(filename, "r");
    if (f == NULL)
    {
        puts("I can't seem to find the words to express myself...");
        return 1;
    }

    do
    {
        fread(buf, 1, sizeof(buf), f);
        fputs(buf, stdout);
    } while (!ferror(f) && !feof(f));

    error = ferror(f);
    fclose(f);
    return error ? 1 : 0;
}
