--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2 (Debian 17.2-1.pgdg120+1)
-- Dumped by pg_dump version 17.2 (Debian 17.2-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: weather_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.weather_data (
    id integer NOT NULL,
    city character varying(50),
    temperature double precision,
    description character varying(100),
    pressure integer,
    humidity integer,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.weather_data OWNER TO postgres;

--
-- Name: weather_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.weather_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.weather_data_id_seq OWNER TO postgres;

--
-- Name: weather_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.weather_data_id_seq OWNED BY public.weather_data.id;


--
-- Name: weather_data id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weather_data ALTER COLUMN id SET DEFAULT nextval('public.weather_data_id_seq'::regclass);


--
-- Data for Name: weather_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.weather_data (id, city, temperature, description, pressure, humidity, "timestamp") FROM stdin;
1	Dakar	26.07	clear sky	1014	61	2024-12-13 10:27:13.880173
2	Thi├¿s	26.36	clear sky	1014	41	2024-12-13 10:27:14.069971
3	Dakar	26.07	clear sky	1013	61	2024-12-13 10:35:49.549817
4	Thi├¿s	26.36	clear sky	1013	41	2024-12-13 10:35:49.745496
\.


--
-- Name: weather_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.weather_data_id_seq', 4, true);


--
-- Name: weather_data weather_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weather_data
    ADD CONSTRAINT weather_data_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

