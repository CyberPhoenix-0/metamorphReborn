#include <stdio.h>
#include <curl/curl.h>
#include <string.h>
#include <stdlib.h>

  /*
    Metamorph Fuzzing Module
    Input : argv[1] de la forme <site.com> 
    Output : fichier xml "url.xml" 
    Argument : <site.com>
    Desc : Find existing pages from wordlist full of urls path
    Syntaxe : module fuzz <site.com>
    */

int make_request(char *url)
{
    CURL *curl = curl_easy_init();
    if(curl) 
    {
        FILE *devnull = fopen("/dev/null", "w+");
        CURLcode response;
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl,CURLOPT_FOLLOWLOCATION,1L);
        curl_easy_setopt(curl, CURLOPT_FAILONERROR, 1L);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, devnull);

        response = curl_easy_perform(curl);
        if(response == CURLE_HTTP_RETURNED_ERROR) 
        {
            return 1;
        }
        else
        {
            return 0;
        }  
    }
    
}

int main(int argc,char *argv[]){
    char filename[30];
    strcat(filename,argv[1]);
    strcat(filename,".xml");
    FILE *xml_file=fopen(filename, "w");
    fprintf(xml_file, "<root>");

    if(argc>2){
        FILE *fichier=NULL;
        fichier=fopen(argv[2], "r");
        if(fichier!=NULL){
        char lines[100];
        while(fgets(lines, sizeof(lines), fichier)!= NULL){
            char *tmp;
            tmp = malloc(sizeof(char) * strlen(lines));
            void *memset(void *str, int c, size_t n);
            memset(tmp, '\0',  strlen(tmp));
            strcat(tmp,argv[1]);
            strcat(tmp,lines);
           
            if (tmp[strlen(tmp)-1] == '\n')
            {
                tmp[strlen(tmp)-1] = '\0';
            }
            if(make_request(tmp)==0){
                printf("%s a retourne 0 \n\n",tmp);
                fprintf(xml_file, "<url>\n<path>");
                fprintf(xml_file, lines);
                fprintf(xml_file, "</path>\n<status>0</status>\n</url>");
            }else{
                printf("%s a retourne 0 \n\n",tmp);
                fprintf(xml_file, "<url>\n<path>");
                fprintf(xml_file, lines);
                fprintf(xml_file, "</path>\n<status>1</status>\n</url>");
            }
        }}else{
            printf("Erreur ouverture fichier");
            return 1;
        
        }
        fclose(fichier);

    }
    else{
        printf("Erreur d'argument");
        return 1;
    }

    fprintf(xml_file, "</root>");
    fclose(xml_file);

}