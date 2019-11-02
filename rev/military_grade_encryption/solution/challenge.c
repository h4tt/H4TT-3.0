#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const unsigned char table[65] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

void scramble (char* in, char* out);

int main (int argc, char* argv[]) {
        char buf[4096];
        char out[5500];
        while (1) {
                printf ("Input to scramble:\n > ");
                scanf ("%4090s", &buf[0]);
                scramble (buf, out);
                printf ("Scrambled input: %s\n", out);
        }
}

void scramble (char* buffer, char* output) {
        size_t len = strlen(buffer);
        char save;
        for (int i = 0; i < len - 1; i++) {
                buffer[i + 1] = buffer[i + 1] ^ buffer[i];
        }
        for (int i = 0; i < len - 1; i += 2) {
                save = buffer[i + 1];
                buffer[i+1] = buffer[i];
                buffer[i] = save;
        }

        /*
         * this is base64 encoding
         */

        const unsigned char *start, *end;
        unsigned char *pos, *out, *in;
        end = buffer + len;
        start = buffer;
        pos = output;
        out = output;
        in = buffer;
        size_t line_len = 0;
        while (end - in >= 3) {
                *pos++ = table[in[0] >> 2];
                *pos++ = table[((in[0] & 0x03) << 4) | (in[1] >> 4)];
                *pos++ = table[((in[1] & 0x0f) << 2) | (in[2] >> 6)];
                *pos++ = table[in[2] & 0x3f];
                in += 3;
                line_len += 4;
                if (line_len >= 76) {
                        *pos++ = '\n';
                        line_len = 0;
                }
        }
        if (end - in) {
                *pos++ = table[in[0] >> 2];
                if (end - in == 1) {
                        *pos++ = table[((in[0] & 0x03) << 4)]; 
                        *pos++ = '=';
                } else {
                        *pos++ = table[((in[0] & 0x03) << 4) | (in[1] >> 4)]; 
                        *pos++ = table[(in[1] & 0x0f) << 2];
                }
                *pos++ = '=';
                line_len += 4;
        }
        if (line_len) 
                *pos++ = '\n';
        *pos++ = '\0';
}
