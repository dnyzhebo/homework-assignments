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
    COUNT(fc.FILM_ID) AS qty_films,
    ctg.NAME
FROM
    PUBLIC.FILM_CATEGORY fc
INNER JOIN
    PUBLIC.CATEGORY ctg ON fc.CATEGORY_ID = ctg.CATEGORY_ID
GROUP BY
    ctg.NAME
ORDER BY
    qty_films DESC;



/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
-- SQL code goes here...


SELECT
    a.first_name||' '||a.last_name actor_name,
    COUNT(r.rental_id) total_rentals
FROM PUBLIC.FILM_ACTOR fa
INNER JOIN public.actor a on a.actor_id = fa.actor_id
INNER JOIN public.film f on f.film_id = fa.film_id
INNER JOIN public.inventory i on i.film_id = f.film_id
INNER JOIN public.rental r on r.inventory_id = i.inventory_id
GROUP BY a.actor_id
ORDER BY 2 DESC
LIMIT 10;

/*
3.
Вивести категорію фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
-- SQL code goes here...

select
    c.name,
    p.amount
from film_category fc
inner join public.category c on fc.category_id = c.category_id
inner join public.inventory i on fc.film_id = i.film_id
inner join public.rental r on i.inventory_id = r.inventory_id
inner join public.payment p on r.rental_id = p.rental_id
LIMIT 10;




/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
-- SQL code goes here...


/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
-- SQL code goes here...
