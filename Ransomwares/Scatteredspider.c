#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void encryptFile(char* filename) {
    FILE* file = fopen(filename, "r+");
    if (file == NULL) {
        perror("Error opening file");
        exit(1);
    }

    fseek(file, 0, SEEK_END);
    long fileSize = ftell(file);
    rewind(file);

    char* buffer = (char*)malloc(fileSize * sizeof(char));
    fread(buffer, sizeof(char), fileSize, file);

    for (int i = 0; i < fileSize; i++) {
        buffer[i] ^= 0xFF; // XOR encryption
    }

    rewind(file);
    fwrite(buffer, sizeof(char), fileSize, file);

    free(buffer);
    fclose(file);
}

int main() {
    char* targetFile = "important_data.txt";
    encryptFile(targetFile);
    printf("File encrypted successfully: %s\n", targetFile);
    return 0;
}
