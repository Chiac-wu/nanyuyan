%{
#include"y.tab.h"
%}
kw 数组|点|线|到|间隔|画
color 红|黄|蓝|绿|白
digit 零|一|二|三|四|五|六|七|八|九|百|十|千|万
letter	[甲乙丙丁戊己庚辛壬癸]
id		{letter}({letter}|{digit})*
number	{digit}+
fu		赋
add 	加
minus   减
mult	乘
divi	除
delim	，|【|】
sp 		[ \15]+

%%
{sp}

"\n"		return CR;

{kw} { 
	if(strcmp(yytext, "数组")==0) return ARRAY; 
	if(strcmp(yytext, "点")==0) return POINT;
	if(strcmp(yytext, "线")==0) return ALINE;
	if(strcmp(yytext, "到")==0) return TO;
	if(strcmp(yytext, "间隔")==0) return INTERVAL;
	if(strcmp(yytext, "画")==0) return DRAW;
}

{id} 		{char * p = (char*)malloc(sizeof(char)*20); strcpy(p, yytext); yylval.text = p; return ID;}

{number} 	{yylval.inum = decodeNum(yytext); return NUM;}

{fu} 		return FU;

{add}		return ADD;
{minus}		return MINUS;
{mult}		return MULT;
{divi} 		return DIVI;

{delim} { 
	if(strcmp(yytext, "【") == 0) return LBRACE;
	if(strcmp(yytext, "】") == 0) return RBRACE;
	if(strcmp(yytext, "，") == 0) return COMMA;
}

{color} { 
	if(strcmp(yytext, "红") == 0) {yylval.inum = 0xFF0000; return COLOR;}
	if(strcmp(yytext, "黄") == 0) {yylval.inum = 0xFFFF00; return COLOR;}
	if(strcmp(yytext, "蓝") == 0) {yylval.inum = 0x0000FF; return COLOR;}
	if(strcmp(yytext, "绿") == 0) {yylval.inum = 0x00FF00; return COLOR;}
	if(strcmp(yytext, "白") == 0) {yylval.inum = 0xFFFFFF; return COLOR;}
}

[0-9]+[a-zA-Z]* perror("invalid identity");

. perror("invalid character");

%%

int convert(char * a) {
	if(strcmp(a, "零")==0) return 0;
	if(strcmp(a, "一")==0) return 1;
	if(strcmp(a, "二")==0) return 2;
	if(strcmp(a, "三")==0) return 3;
	if(strcmp(a, "四")==0) return 4; 
	if(strcmp(a, "五")==0) return 5;
	if(strcmp(a, "六")==0) return 6;
	if(strcmp(a, "七")==0) return 7;
	if(strcmp(a, "八")==0) return 8;
	if(strcmp(a, "九")==0) return 9;
	if(strcmp(a, "十")==0) return 10;
	if(strcmp(a, "百")==0) return 100;
	if(strcmp(a, "千")==0) return 1000;
	if(strcmp(a, "万")==0) return 10000;
	return -1;
}
int decodeNum(char * s) {
	char sp[20][4];
	memset(sp, sizeof(sp), '\0');
	//split 
	for(int i = 0; s[i]!='\0';i++) {
		sp[i/3][i%3] = s[i];
		sp[i/3][3] = '\0';
	}
	int sum = 0;

	for(int i=0;i<strlen(s)/3;i++)
	{
		int b = convert(sp[i]);
		if(b == 0) continue;
		int c = convert(sp[i+1]);
		if(c != -1&&i+1<strlen(s)/3) {
			sum+=b*c;
			i++;
		}
		else {
			sum+=b;
		}
	}
	return sum;
}
