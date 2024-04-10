/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
-- SQL code goes here...

SELECT
    COUNT(fc.film_id) AS qty_films,
    ctg.name
FROM
    public.film_category fc
INNER JOIN public.category ctg ON fc.category_id = ctg.category_id
GROUP BY ctg.name
ORDER BY qty_films DESC;

/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
-- SQL code goes here...

SELECT
    a.first_name || ' ' || a.last_name AS actor_name,
    COUNT(r.rental_id) AS total_rentals
FROM
    public.film_actor fa
INNER JOIN public.actor a ON a.actor_id = fa.actor_id
INNER JOIN public.film f ON f.film_id = fa.film_id
INNER JOIN public.inventory i ON i.film_id = f.film_id
INNER JOIN public.rental r ON r.inventory_id = i.inventory_id
GROUP BY
    a.actor_id
ORDER BY
    total_rentals DESC
LIMIT 10;

/*
3.
Вивести категорію фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
-- SQL code goes here...

SELECT
    c.name AS category_name,
    SUM(p.amount) AS total_amount
FROM
    film_category fc
INNER JOIN public.category c ON fc.category_id = c.category_id
INNER JOIN public.inventory i ON fc.film_id = i.film_id
INNER JOIN public.rental r ON i.inventory_id = r.inventory_id
INNER JOIN public.payment p ON r.rental_id = p.rental_id
GROUP BY
    c.name
ORDER BY
    total_amount DESC
LIMIT 1;

/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
-- SQL code goes here...

SELECT
    f.title
FROM film f
LEFT JOIN public.inventory i on f.film_id = i.film_id
WHERE i.inventory_id IS NULL;

/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
-- SQL code goes here...

SELECT
    COUNT(fa.film_id) qty_films,
    a.first_name || ' ' || a.last_name AS actor_name
FROM
    public.film_actor fa
INNER JOIN public.actor a ON a.actor_id = fa.actor_id
INNER JOIN public.film f ON f.film_id = fa.film_id
INNER JOIN public.film_category fc ON f.film_id = fc.film_id
INNER JOIN public.category ctg ON fc.category_id = ctg.category_id
WHERE ctg.name = 'Children'
GROUP BY a.actor_id
ORDER BY qty_films DESC
LIMIT 3;