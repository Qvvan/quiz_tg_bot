--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0
-- Dumped by pg_dump version 16.0

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: now; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.now (
    quest_id bigint NOT NULL,
    tg_id bigint NOT NULL
);


ALTER TABLE public.now OWNER TO postgres;

--
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
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    tg_id bigint NOT NULL,
    name text NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_question; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_question (
    quest_id bigint NOT NULL,
    tg_id bigint NOT NULL,
    status text DEFAULT 'NO'::text NOT NULL
);


ALTER TABLE public.user_question OWNER TO postgres;

--
-- Name: wrong_list; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wrong_list (
    quest_id bigint NOT NULL,
    tg_id bigint NOT NULL
);


ALTER TABLE public.wrong_list OWNER TO postgres;

--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- Data for Name: now; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.now (quest_id, tg_id) FROM stdin;
\.


--
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
73	Для кодирования букв М, У, Х, А использован неравномерный двоичный код, допускающий однозначное декодирование. Для кодирования букв У и М использовали кодовые слова 11 и 10 соответственно. Какова минимальная возможная cумма для букв У, Х, А?	6	{5,4,7}	\N
74	Как к числу 101 типа int добавить бит раный '1'?	str(101) + '1'	{"101 + 1","101 + '1'","str(101, 1)"}	\N
75	Как взять последние две цифры у числа A?	A  % 100	{A[-2],A[:-2],A[::-2]}	\N
76	Как взять первые две цифры у числа А?	A // 100	{"A[0,2]",A[2:],A[::2]}	\N
77	Как перевернуть строку А?	A[::-1]	{A[-1::],A[:-1:],"A[0,-1,-1]"}	\N
78	В палитре используется 120 цветов, чему ровна минимальная битовая глубина кодирования?	7	{1,6,120}	\N
79	В изображении битовая глубина кодирования равна 11, какое максимальное количество цветов может содержаться в палитре?	2048	{11,1024,1}	\N
80	Сколько будет 16384 бит в Кбайт?	2	{16,2048,4}	\N
81	Как импортировать функцию product?	from itertools import product	{"import product","from product","import itertools from product"}	\N
82	Как импортировать функцию permutations?	from itertools import permutations	{"import permutations","from permutations","import itertools from permutations"}	\N
83	Как проверить, что две гласные буквы 'А' есть в переменной stroka?	'AA' in stroka	{"'A' = S","AA in S","'AA' find S"}	\N
84	В чем измеряется частота дискретизации?	Гц	{кГц,секунды,бит}	\N
85	Пароль состоит из 11 символов и содержащий только символы А, Б, В, Г, Д, Е. Сколько бит занимает пароль?	33	{66,22,44}	\N
86	Пароль состоит из 11 символов и содержащий только символы латинского алфавита и цифры от 1 до 9. Сколько байт занимает пароль?	9	{8,7,10}	\N
87	Как создать строку, состоящую из 55 цифр 5 и последняя цифра в строке — цифра 7	s = 55 * '5' + '7'	{"s = 55 * 5 + 7","s =5 * '55' + 7","s = 55 * '5' + 7"}	\N
88	Как в строке S, сделать единичную замену 5 на 2?	s.replace('5', '2', 1)	{"s.replace(5,2,1)","s.replace('5', '2')",s[5:2:1]}	\N
89	Как проверить, что в строке S есть последовательность из трех подряд идущих 3?	'333' in S	{"'333' == S","333 in S","'333' find S"}	\N
90	Сколько единиц в крайнем левом байте маски 255.255.255.0	8	{24,16,4}	\N
34	Какой метод используется для замены символов в строке?	replace()	{substring(),swap(),substitute()}	\N
35	Как импортировать все функции с библиотеки math?	from math import *	{"from math import math","from math import all","import math.*"}	\N
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
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (tg_id, name) FROM stdin;
323993202	Иван
\.


--
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
2	323993202	NO
23	323993202	NO
28	323993202	NO
32	323993202	NO
33	323993202	NO
31	323993202	NO
26	323993202	NO
24	323993202	NO
1	323993202	NO
8	323993202	NO
10	323993202	NO
18	323993202	NO
20	323993202	NO
29	323993202	NO
3	323993202	NO
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
\.


--
-- Data for Name: wrong_list; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wrong_list (quest_id, tg_id) FROM stdin;
\.


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.question_id_seq', 90, true);


--
-- Name: question question_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_pkey PRIMARY KEY (id);


--
-- Name: question unique_question; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT unique_question UNIQUE (question);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (tg_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

