#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_words(char* words)
{
	char cmd[128] = "cowsay -f parrot -t \"Hi, I'm your friendly neighborhood parrot (new and improved)!\"";
	char wordbuf[64] = "Here's what I have to say: ";
	strcat(wordbuf, words);  /* !!! */

	/* Fun ASCII parrot. No danger here! */
	system(cmd);
	puts(wordbuf);
}

int main(int argc, char** argv)
{
    if (argc < 2)
    {
        puts("I don't run races anymore. They're too dangerous!");
        printf("Tell me what you want me to say like this: %s WORDS\n", argv[0]);
        return 1;
    }
    print_words(argv[1]);
    return 0;
}
