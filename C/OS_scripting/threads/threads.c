#include <stdio.h> //input/output
#include <stdlib.h> //Библиотека для типов
#include <unistd.h> //Библиотека для нек. сист вызовов
#include <string.h> //хз, что-то по строкам
#include <sys/wait.h> //Сист. вызов wait
#include <fcntl.h> //Для файлов


int main(int argc, char* argv[])
{
    // printf("pid:(%d)\n", (int)getpid()); //Родительский процесс
    int new_process = fork();
    if (new_process < 0) {
        fprintf(stderr, "Ошибка fork\n");
        exit(1);
    }
    else if (new_process == 0) {
        close(STDOUT_FILENO); //Закрывает стандартный вывод
        open("./test.output", O_CREAT|O_WRONLY|O_TRUNC, S_IRWXU);

        char* args[argc];
        // printf("%d\n", argc);
        for (int i = 1; i < argc; i++) {
            args[i - 1] = strdup(argv[i]);
            // printf("%s\n", argv[i]);
        }
        args[argc - 1] = NULL;   
        execvp(args[0], args); 
    }
    else {
        int rc_wait = wait(NULL);
    }
    return 0;
    
}