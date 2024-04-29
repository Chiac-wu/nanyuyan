%{
#include<stdio.h>
#include<string.h>
int yylex(void);
void yyerror(char *);
int decodeNum(char *);
int registerId(char *);

int * r[10];
%}

%union{
    int inum;
    char * text;
    void * pointer;
}

%token <inum> NUM COLOR
%token <text>ID 
%token FU CR ADD MINUS MULT DIVI ARRAY POINT ALINE LBRACE RBRACE COMMA TO INTERVAL DRAW

%type <inum> exp term tterm factor ffactor
%type <pointer> obj newarray

%%

    input: line
         | input line
         ;

    line: assignment CR
        | plot CR
        | CR
        ;
        

    assignment: ID FU exp {
            // printf("%s赋为%d\n", $1,$3);
            int * t = (int*) malloc(sizeof(int));
            *t = $3;
            r[registerId($1)] = t;
        }
              | ID FU obj {
                    // printf("%s赋为对象\n", $1);
                    r[registerId($1)] = $3;
                }
              ;

    exp: term tterm {$$ = $1+$2;};

    tterm: ADD term tterm {$$ = $2+$3;}
         | MINUS term tterm {$$ = -($2+$3);}
         | {$$ = 0;}
         ;
    
    term: factor ffactor {$$ = $1*$2;};

    ffactor: MULT factor ffactor {$$ = $2*$3;}
           | {$$ = 1;}
           ;


    factor: ID {
            $$ = *r[registerId($1)];
        }  
          | NUM 
          ;

    obj: newarray {
        $$ = $1;
    }
    //    | newline
    //    | newpoint
       ;

    newarray: ARRAY LBRACE NUM TO exp COMMA INTERVAL NUM RBRACE {
        int l = ($5-$3)%$8==0?($5-$3)/$8:($5-$3)/$8+1;
        int * t = (int*)malloc(sizeof(int)*(l+1));
        int j = $3;
        for(int i = 0; i<l; i++){
            t[i] = j;
            j+=$8;
        }
        t[l]='\0';
        $$ = (void*)t;
    }
            | ARRAY LBRACE NUM TO exp RBRACE {
                int l = $5-$3;
                int * t = (int*)malloc(sizeof(int)*(l+1));
                int j = $3;
                for(int i = 0; i<l; i++){
                    t[i] = j;
                    j++;
                }
                t[l]='\0';
                $$ = (void*)t;
            }
            ;

    plot: DRAW LBRACE ID COMMA ID RBRACE {
            int * x = r[registerId($3)];
            int * y = r[registerId($5)];
            while(*x!='\0') {
                printf("(%d, %d)\n", *x,*y);
                x++;
                y++;
            }
        };
        |
        DRAW LBRACE ID COMMA ID COMMA COLOR RBRACE {
            int * x = r[registerId($3)];
            int * y = r[registerId($5)];
            while(*x!='\0') {
                printf("(%d, %d, %lX)\n", *x,*y, (long unsigned int)$7);
                x++;
                y++;
            }
        };

    

%%

void yyerror(char *str){
    fprintf(stderr,"error:%s\n",str);
}

int yywrap(){
    return 1;
}

int registerId(char* s) {
    if(strcmp(s, "甲") == 0) return 0;
    if(strcmp(s, "乙") == 0) return 1;
    if(strcmp(s, "丙") == 0) return 2;
    if(strcmp(s, "丁") == 0) return 3;
    if(strcmp(s, "戊") == 0) return 4;
    if(strcmp(s, "己") == 0) return 5;
    if(strcmp(s, "庚") == 0) return 6;
    if(strcmp(s, "辛") == 0) return 7;
    if(strcmp(s, "壬") == 0) return 8;
    if(strcmp(s, "癸") == 0) return 9;
}

int main()
{
    yyparse();
}