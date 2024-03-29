--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0
-- Dumped by pg_dump version 16.0

-- Started on 2024-03-29 11:38:00

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 33382)
-- Name: now; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.now (
    quest_id bigint NOT NULL,
    tg_id bigint NOT NULL
);


ALTER TABLE public.now OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 33385)
-- Name: question; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.question (
    id integer NOT NULL,
    question text NOT NULL,
    answer text NOT NULL,
    wrong text[],
    path_img text
);


ALTER TABLE public.question OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 33390)
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.question_id_seq OWNER TO postgres;

--
-- TOC entry 4813 (class 0 OID 0)
-- Dependencies: 217
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- TOC entry 218 (class 1259 OID 33391)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    tg_id bigint NOT NULL,
    name text NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 33396)
-- Name: user_question; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_question (
    quest_id bigint NOT NULL,
    tg_id bigint NOT NULL,
    status text DEFAULT 'NO'::text NOT NULL
);


ALTER TABLE public.user_question OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 33402)
-- Name: wrong_list; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wrong_list (
    quest_id bigint NOT NULL,
    tg_id bigint NOT NULL
);


ALTER TABLE public.wrong_list OWNER TO postgres;

--
-- TOC entry 4650 (class 2604 OID 33405)
-- Name: question id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- TOC entry 4801 (class 0 OID 33382)
-- Dependencies: 215
-- Data for Name: now; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.now (quest_id, tg_id) FROM stdin;
3	323993202
\.


--
-- TOC entry 4802 (class 0 OID 33385)
-- Dependencies: 216
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.question (id, question, answer, wrong, path_img) FROM stdin;
11	Какой метод используется для удаления элемента из списка по индексу?	pop()	{remove(),discard(),delete()}	\N
12	Каким образом вы можете округлить число в переменной digit до ближайшего целого в Python?	round(digit)	{round(digit),roundDigit(),roundUp(digit)}	\N
13	Каким образом вы можете проверить, принадлежит ли элемент списку в Python?	in	{belongs(),contains(),inList()}	\N
14	Какой оператор используется для логического 'ИЛИ' в Python?	or	{||,&&,&}	\N
15	Каким образом вы можете прервать выполнение цикла в Python?	break	{end(),stop(),finish()}	\N
17	Какая функция используется для получения наибольшего числа из списка?	max()	{maximum(),largest(),biggest()}	\N
22	С помощью какой функции можно перевести число в двоичную систему счисления?	bin()	{binify(),binary(),toBinary()}	\N
21	Как проверить, является ли число N четным?	n % 2 == 0	{"num % 2 = 0",num.isEven(),isEven(num)}	\N
25	С помощью какого метода можно посчитать все цифры "1" в переменной A = "101011"?	A.count("1")	{A.counter(1),"count(A, 1)","count(1, A)"}	\N
27	Какой оператор используется для объединения двух или более списков в Python?	+	{append(),concat(),join()}	\N
2	Какой оператор используется для логического 'И' в Python?	and	{&&,||,==}	\N
23	Как перевести число 101 из двоичной СС, в 10 СС в Python?	int("101", 2)	{"int(101, 2)",int(binary),toInt(101)}	\N
28	Как создать пустой словарь empty_dict в Python?	empty_dict = {}	{"{}",empty(),null()}	\N
32	Чего не хватает в данном коде?\\nfor i in "hello world"\\n    print(i)	:	{colon,==,indentation}	\N
33	Сколько аргументов принимает функция range?	3	{1,2,5}	\N
31	Как в Python получить остаток от деления переменной A на B?	A%B	{mod(),%%,remainder()}	\N
26	Что будет в переменной N, после записи N = bin(10)?	0b1010	{1010,1010b,0b101}	\N
24	Какой тип данных примет переменная N, если в нее записать bin(10)?	str	{s,string,text}	\N
1	Какой символ используется для обозначения комментария в Python?	#	{//,/#,/*}	\N
8	Как получить длину строки some_str в Python?	len(some_str)	{length(),size(),count()}	\N
10	Каким образом вы можете импортировать библиотеку math в Python?	import math	{"import library math","use math","from math import module"}	\N
18	Какая функция используется для получения суммы чисел списка?	sum()	{addUp(),total(),summarize()}	\N
20	Какая функция используется для получения наименьшего числа из списка?	min()	{minimum(),smallest(),littlest()}	\N
29	Как удалить элемент с индексом 3 из списка lst в Python?	lst.pop(3)	{lst.remove(3),lst.delete(3),"remove(lst, 3)"}	\N
3	Каким образом вы можете объявить функцию func в Python?	def func():	{"func() def :","define func():",func():}	\N
4	Какой оператор используется для проверки равенства двух значений в Python?	==	{===,=,!=}	\N
5	Какой метод используется для добавления элемента в список?	append()	{insert(),extend(),add()}	\N
7	Какой тип данных используется для представления текстовой информации в Python?	str	{string,s,lenght}	\N
9	Как получить последний элемент списка lst в Python?	lst[-1]	{lst.get(-1),lst[::-1],lst.last()}	\N
30	Как получить только целую часть результата деления переменной A на B в Python?	A//B	{/,div(),floor()}	\N
19	Когда вы используете k = input(), к какому типу данных будет отнесена переменная k?	str	{integer,text,int}	\N
16	Каким образом можно извлечь подстроку "cde" из строки, представленной переменной s = "abcdefg" в Python?	s[2:5]	{"s.substring(2, 5)","s.slices(2, 5)","s.extract(2, 5)"}	\N
6	Как создать пустой список lst в Python?	lst=[]	{"list= lst()","lst = list[]","list = lst[]"}	\N
72	Для кодирования букв М, У, Х, А использован неравномерный двоичный код, допускающий однозначное декодирование. Для кодирования букв У и М использовали кодовые слова 11 и 10 соответственно. Какова минимальная возможная длина буквы Х?	01	{1,0,10}	\N
74	Как к числу 101 типа int добавить бит раный '1'?	str(101) + '1'	{"101 + 1","101 + '1'","str(101, 1)"}	\N
76	Как взять первые две цифры у числа А?	A // 100	{"A[0,2]",A[2:],A[::2]}	\N
77	Как перевернуть строку А?	A[::-1]	{A[-1::],A[:-1:],"A[0,-1,-1]"}	\N
79	В изображении битовая глубина кодирования равна 11, какое максимальное количество цветов может содержаться в палитре?	2048	{11,1024,1}	\N
82	Как импортировать функцию permutations?	from itertools import permutations	{"import permutations","from permutations","import itertools from permutations"}	\N
83	Как проверить, что две гласные буквы 'А' есть в переменной stroka?	'AA' in stroka	{"'A' = S","AA in S","'AA' find S"}	\N
84	В чем измеряется частота дискретизации?	Гц	{кГц,секунды,бит}	\N
86	Пароль состоит из 11 символов и содержащий только символы латинского алфавита и цифры от 1 до 9. Сколько байт занимает пароль?	9	{8,7,10}	\N
88	Как в строке S, сделать единичную замену 5 на 2?	s.replace('5', '2', 1)	{"s.replace(5,2,1)","s.replace('5', '2')",s[5:2:1]}	\N
90	Сколько единиц в крайнем левом байте маски 255.255.255.0	8	{24,16,4}	\N
81	Для кодирования букв М, У, Х, А использован неравномерный двоичный код, допускающий однозначное декодирование. Для кодирования букв У и М использовали кодовые слова 11 и 10 соответственно. Какова минимальная возможная cумма для букв У, Х, А?	6	{5,4,7}	\N
73	Как импортировать функцию product?	from itertools import product	{"import product","from product","import itertools from product"}	\N
75	Пароль состоит из 11 символов и содержащий только символы А, Б, В, Г, Д, Е. Сколько бит занимает пароль?	33	{66,22,44}	\N
85	Как взять последние две цифры у числа A?	A  % 100	{A[-2],A[:-2],A[::-2]}	\N
78	Как создать строку, состоящую из 55 цифр 5 и последняя цифра в строке — цифра 7	s = 55 * '5' + '7'	{"s = 55 * 5 + 7","s =5 * '55' + 7","s = 55 * '5' + 7"}	\N
87	В палитре используется 120 цветов, чему ровна минимальная битовая глубина кодирования?	7	{1,6,120}	\N
34	Какой метод используется для замены символов в строке?	replace()	{substring(),swap(),substitute()}	\N
35	Как импортировать все функции с библиотеки math?	from math import *	{"from math import math","from math import all","import math.*"}	\N
89	Сколько будет 16384 бит в Кбайт?	2	{16,2048,4}	\N
80	Как проверить, что в строке S есть последовательность из трех подряд идущих 3?	'333' in S	{"'333' == S","333 in S","'333' find S"}	\N
36	Как проверить, что число X не принадлежит списку lst?	x not in lst	{"no in lst","in not lst",inList()}	\N
37	Сколько аргументов принимает метод replace()?	3	{5,2,1}	\N
38	Мы хотим написать программу, которая выводит "Да", если число больше, и "Нет", если меньше, чего нехватает в коде?\\na = 5 > 10\\nif a:\\n    print("YES")\\nprint("NO")	else:	{self,elif,"else if"}	\N
39	Что выведет данное выражение?\\n[num if num > 2 else 0 for num in [1,3,5,2]	[0,3,5,0]	{"[1, 3, 5, 2]","[0, 3, 5, 0]","[1, 0, 1, 1]"}	\N
40	Какая функция округлит число в большую сторону?	ceil()	{floor(),roundDown(),down()}	\N
41	Какая функция округлит число в меньшую сторону?	floor()	{ceil(),roundUp(),up()}	\N
42	Какая функция переводит число в восмиричную систему счисления?	oct()	{octal(),toOct(),base8()}	\N
43	Какая функция переводит число в шестнадцатиричную систему счисления?	hex()	{hexadecimal(),toHex(),base16()}	\N
44	Какой метод списка используется для нахождения индекса числа?	index()	{find(),locate(),getPosition()}	\N
45	Какой метод отсортирует список в Python?	sort()	{sorted(),order(),orderList()}	\N
46	Нужно посчитать количество чисел, что нужно записать вместо pass?\\ncount = 0\\nfor i in range(10):\\n pass	count += 1	{"count +== 1","count = count(1)",count++}	\N
47	Нужно посчитать сумму чисел, что нужно записать вместо pass?\\nsumma = 0\\nfor i in range(10):\\n pass	summa += i	{"sum == i","sum = summa + i","sum =+ i"}	\N
48	Что нужно исправить в данном коде?\\ncount = 0\\nfor i in range(10):\\n count = 1\\nprint(count)	count += 1	{"count ++ 1","count = 1","count =+ 1"}	\N
49	Что выведет функция print()?\\ncount = 0\\nfor i in range(10):\\n count = 1\\nprint(count)	1	{1,0,count}	\N
50	Что нужно исправить в данном коде?\\nsum = 1\\nfor i in range(10):\\n sum += i	sum = 0	{"sum = 1","sum = 0","sum = 1 + i"}	\N
51	Что выведет функция print()?\\numn = 0\\nfor i in range(10):\\n umn = umn * i\\nprint(umn)	0	{0,"null",1}	\N
52	Какие типы данных являются неизменяемыми (immutable) в Python?	str и tuple	{"str и list","dict и tuple","tuple и list"}	\N
53	Какой оператор используется для логического "не" в Python?	not	{&&,!,!=}	\N
54	Какой метод используется для удаления элемента из списка по значению?	remove()	{delete(),pop(),discard()}	\N
55	Какой результат будет у выражения 10 / 3 в Python?	3.0	{3.3333,3,3.33}	\N
56	Какой метод используется для сортировки списка в порядке убывания?	sort(reverse=True)	{sorted(reverse=True),sort_desc(),descending()}	\N
57	Каков результат выполнения выражения 2 ** 3 в Python?	8	{6,12,9}	\N
58	Как получить срез списка с шагом 2 в Python?	list[::2]	{list[1::2],"list[::2,1]",list[1:][2]}	\N
59	Какой результат будет у выражения "hello" + 2 в Python?	TypeError	{hello2,Error,hellohello}	\N
60	Какой метод используется для получения значения по ключу из словаря?	get()	{value()," retrieve()",fetch()}	\N
61	Каким образом можно узнать тип переменной в Python?	type(variable)	{variable.type(),typeOf(variable),typeof(variable)}	\N
62	Какие методы используются для работы со строками в Python?	upper(), lower(), split()	{"add(), remove(), contains()","push(), pop(), concat()","join(), length(), reverse()"}	\N
63	Какой метод используется для разделения строки на подстроки по определенному разделителю?	split()	{divide(),separate(),slice()}	\N
64	Как создать копию списка в Python, чтобы изменения в одном списке не влияли на другой?	list.copy()	{list.clone(),copy(list),list[:]}	\N
65	Что такое PEP 8 в контексте языка программирования Python?	Стиль кодирования для языка Python	{"Последняя версия Python","Название стандартной библиотеки","Методология тестирования в Python"}	\N
66	Что такое рекурсия в программировании?	Вызов функцией самой себя	{"Техника шифрования данных","Автоматизированное тестирование","Способ объединения нескольких файлов"}	\N
67	Каким образом можно узнать количество элементов в списке в Python?	С использованием функции len()	{"Используя метод size()","Просматривая список вручную","Применяя функцию count()"}	\N
68	Что делает оператор "pass" в Python?	Не выполняет никаких действий; используется как заполнитель в структурах, где синтаксически требуется блок кода	{"Завершает выполнение программы","Передает управление следующему блоку кода","Вызывает ошибку синтаксиса"}	\N
69	Как в Python выполнить сортировку списка lst в порядке возрастания?	sorted(lst)	{sort_list(lst),list.sort(),ascending_sort(lst)}	\N
70	Как в Python проверить, содержится ли подстрока 'abc' в строке s?	if 'abc' in s:	{"if s.contains('abc'):","if s.include('abc'):","if s.indexOf('abc'):"}	\N
71	Чего не хватает в данном коде?	if, in | in, if	\N	img/1.png
\.


--
-- TOC entry 4804 (class 0 OID 33391)
-- Dependencies: 218
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (tg_id, name) FROM stdin;
323993202	Иван
5207009333	Никита
1095424968	Михаил
948817209	Катерина Романовна
\.


--
-- TOC entry 4805 (class 0 OID 33396)
-- Dependencies: 219
-- Data for Name: user_question; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_question (quest_id, tg_id, status) FROM stdin;
11	323993202	NO
12	323993202	NO
13	323993202	NO
14	323993202	NO
15	323993202	NO
17	323993202	NO
22	323993202	NO
21	323993202	NO
25	323993202	NO
27	323993202	NO
23	323993202	NO
28	323993202	NO
32	323993202	NO
33	323993202	NO
31	323993202	NO
26	323993202	NO
24	323993202	NO
8	323993202	NO
10	323993202	NO
18	323993202	NO
20	323993202	NO
29	323993202	NO
4	323993202	NO
5	323993202	NO
7	323993202	NO
9	323993202	NO
30	323993202	NO
19	323993202	NO
16	323993202	NO
6	323993202	NO
72	323993202	NO
73	323993202	NO
74	323993202	NO
75	323993202	NO
76	323993202	NO
77	323993202	NO
78	323993202	NO
79	323993202	NO
80	323993202	NO
81	323993202	NO
82	323993202	NO
83	323993202	NO
84	323993202	NO
85	323993202	NO
86	323993202	NO
87	323993202	NO
88	323993202	NO
89	323993202	NO
90	323993202	NO
34	323993202	NO
35	323993202	NO
36	323993202	NO
37	323993202	NO
38	323993202	NO
39	323993202	NO
40	323993202	NO
41	323993202	NO
42	323993202	NO
43	323993202	NO
44	323993202	NO
45	323993202	NO
46	323993202	NO
47	323993202	NO
48	323993202	NO
49	323993202	NO
50	323993202	NO
51	323993202	NO
52	323993202	NO
53	323993202	NO
54	323993202	NO
55	323993202	NO
56	323993202	NO
57	323993202	NO
58	323993202	NO
59	323993202	NO
60	323993202	NO
61	323993202	NO
62	323993202	NO
63	323993202	NO
64	323993202	NO
65	323993202	NO
66	323993202	NO
67	323993202	NO
68	323993202	NO
69	323993202	NO
70	323993202	NO
71	323993202	NO
2	323993202	YES
1	323993202	YES
3	323993202	YES
75	5207009333	NO
76	5207009333	NO
77	5207009333	NO
78	5207009333	NO
79	5207009333	NO
80	5207009333	NO
81	5207009333	NO
82	5207009333	NO
83	5207009333	NO
84	5207009333	NO
85	5207009333	NO
86	5207009333	NO
87	5207009333	NO
88	5207009333	NO
89	5207009333	NO
90	5207009333	NO
11	5207009333	YES
12	5207009333	YES
72	1095424968	NO
73	1095424968	NO
74	1095424968	NO
75	1095424968	NO
76	1095424968	NO
77	1095424968	NO
78	1095424968	NO
79	1095424968	NO
80	1095424968	NO
81	1095424968	NO
82	1095424968	NO
83	1095424968	NO
84	1095424968	NO
85	1095424968	NO
86	1095424968	NO
87	1095424968	NO
88	1095424968	NO
89	1095424968	NO
90	1095424968	NO
34	1095424968	NO
35	1095424968	NO
36	1095424968	NO
37	1095424968	NO
38	1095424968	NO
39	1095424968	NO
40	1095424968	NO
41	1095424968	NO
42	1095424968	NO
43	1095424968	NO
44	1095424968	NO
45	1095424968	NO
46	1095424968	NO
47	1095424968	NO
48	1095424968	NO
49	1095424968	NO
50	1095424968	NO
51	1095424968	NO
52	1095424968	NO
53	1095424968	NO
54	1095424968	NO
55	1095424968	NO
56	1095424968	NO
57	1095424968	NO
58	1095424968	NO
59	1095424968	NO
60	1095424968	NO
61	1095424968	NO
62	1095424968	NO
63	1095424968	NO
64	1095424968	NO
65	1095424968	NO
66	1095424968	NO
67	1095424968	NO
68	1095424968	NO
69	1095424968	NO
70	1095424968	NO
71	1095424968	NO
75	948817209	NO
76	948817209	NO
77	948817209	NO
78	948817209	NO
79	948817209	NO
11	948817209	YES
12	948817209	YES
13	948817209	YES
14	948817209	YES
15	948817209	YES
17	948817209	YES
22	948817209	YES
21	948817209	YES
25	948817209	YES
27	948817209	YES
2	948817209	YES
23	948817209	YES
28	948817209	YES
32	948817209	YES
33	948817209	YES
31	948817209	YES
26	948817209	YES
24	948817209	YES
1	948817209	YES
8	948817209	YES
10	948817209	YES
18	948817209	YES
20	948817209	YES
29	948817209	YES
11	1095424968	YES
12	1095424968	YES
13	1095424968	YES
14	1095424968	YES
15	1095424968	YES
17	1095424968	YES
22	1095424968	YES
21	1095424968	YES
25	1095424968	YES
27	1095424968	YES
2	1095424968	YES
23	1095424968	YES
28	1095424968	YES
32	1095424968	YES
33	1095424968	YES
31	1095424968	YES
26	1095424968	YES
24	1095424968	YES
1	1095424968	YES
8	1095424968	YES
10	1095424968	YES
18	1095424968	YES
20	1095424968	YES
29	1095424968	YES
3	1095424968	YES
4	1095424968	YES
5	1095424968	YES
7	1095424968	YES
9	1095424968	YES
30	1095424968	YES
19	1095424968	YES
16	1095424968	YES
6	1095424968	YES
80	948817209	NO
81	948817209	NO
82	948817209	NO
83	948817209	NO
84	948817209	NO
85	948817209	NO
86	948817209	NO
87	948817209	NO
88	948817209	NO
89	948817209	NO
90	948817209	NO
13	5207009333	YES
14	5207009333	YES
15	5207009333	YES
17	5207009333	YES
22	5207009333	YES
21	5207009333	YES
25	5207009333	YES
27	5207009333	YES
2	5207009333	YES
23	5207009333	YES
28	5207009333	YES
32	5207009333	YES
33	5207009333	YES
31	5207009333	YES
26	5207009333	YES
24	5207009333	YES
1	5207009333	YES
8	5207009333	YES
10	5207009333	YES
18	5207009333	YES
20	5207009333	YES
29	5207009333	YES
3	5207009333	YES
4	5207009333	YES
5	5207009333	YES
7	5207009333	YES
9	5207009333	YES
30	5207009333	YES
19	5207009333	YES
16	5207009333	YES
6	5207009333	YES
72	5207009333	YES
73	5207009333	YES
74	5207009333	YES
34	5207009333	YES
35	5207009333	YES
36	5207009333	YES
37	5207009333	YES
38	5207009333	YES
39	5207009333	YES
40	5207009333	YES
41	5207009333	YES
42	5207009333	YES
43	5207009333	YES
44	5207009333	YES
45	5207009333	YES
46	5207009333	YES
47	5207009333	YES
48	5207009333	YES
49	5207009333	YES
50	5207009333	YES
51	5207009333	YES
52	5207009333	YES
53	5207009333	YES
54	5207009333	YES
55	5207009333	YES
56	5207009333	YES
57	5207009333	YES
58	5207009333	YES
59	5207009333	YES
60	5207009333	YES
61	5207009333	YES
62	5207009333	YES
63	5207009333	YES
64	5207009333	YES
65	5207009333	YES
66	5207009333	YES
67	5207009333	YES
68	5207009333	YES
69	5207009333	YES
70	5207009333	YES
71	5207009333	YES
3	948817209	YES
4	948817209	YES
5	948817209	YES
7	948817209	YES
9	948817209	YES
30	948817209	YES
19	948817209	YES
16	948817209	YES
6	948817209	YES
72	948817209	YES
73	948817209	YES
74	948817209	YES
34	948817209	YES
35	948817209	YES
36	948817209	YES
37	948817209	YES
38	948817209	YES
39	948817209	YES
40	948817209	YES
41	948817209	YES
42	948817209	YES
43	948817209	YES
44	948817209	YES
45	948817209	YES
46	948817209	YES
47	948817209	YES
48	948817209	YES
49	948817209	YES
50	948817209	YES
51	948817209	YES
52	948817209	YES
53	948817209	YES
54	948817209	YES
55	948817209	YES
56	948817209	YES
57	948817209	YES
58	948817209	YES
59	948817209	YES
60	948817209	YES
61	948817209	YES
62	948817209	YES
63	948817209	YES
64	948817209	YES
65	948817209	YES
66	948817209	YES
67	948817209	YES
68	948817209	YES
69	948817209	YES
70	948817209	YES
71	948817209	YES
\.


--
-- TOC entry 4806 (class 0 OID 33402)
-- Dependencies: 220
-- Data for Name: wrong_list; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wrong_list (quest_id, tg_id) FROM stdin;
1	323993202
2	323993202
\.


--
-- TOC entry 4814 (class 0 OID 0)
-- Dependencies: 217
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.question_id_seq', 90, true);


--
-- TOC entry 4653 (class 2606 OID 33407)
-- Name: question question_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_pkey PRIMARY KEY (id);


--
-- TOC entry 4655 (class 2606 OID 33414)
-- Name: question unique_question; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT unique_question UNIQUE (question);


--
-- TOC entry 4657 (class 2606 OID 33409)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (tg_id);


--
-- TOC entry 4812 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2024-03-29 11:38:00

--
-- PostgreSQL database dump complete
--

