# Поиск по параметрическому запросу
Рекомендательная система выбирает для пользователя подходящую ему породу собак.  
**lab02.json** - файл содержит описание пород собак с их характеристиками.  
**lab05.py** - код основной программы.    
Интерфейс приложения:  
![alt text](https://sun9-36.userapi.com/impf/dSfeD1l863WXe_kfreylpCNLlRLbWvIn6Bx6Eg/ODnCIG4fML4.jpg?size=996x440&quality=96&proxy=1&sign=f60b1b6356471f0c684d40cae0d6af9a&type=album)  
Пользователь вводит характеристики собаки. Он оценивает некоторые её характеристики по пятибальной шкале, выбирает размер и указывает, собирается ли он держать собаку в квартире. Затем нажимает кнопку "Найти".  
![alt text](https://sun9-23.userapi.com/impf/9-4KRSMQcZKPDddqrx8Kk6DeYdHeK4tD-Tlm3w/oulL3yw8wyg.jpg?size=992x442&quality=96&proxy=1&sign=72af0b3ba2e12c5653105cb3ae9e511c&type=album)  
Делаются первые рекомендации. Алгоритм поиска рекомендаций - поиск по эталону из лр 4.  
Пользователь может высказать свое мнение о рекомендациях. Отметить, какие породы ему понравились, а какие нет.  
![alt text](https://sun9-62.userapi.com/impf/ZYuQma3hES0jikDkplqbxA6FCWKqiPD0Cl-Htw/ZszZHBJPCvg.jpg?size=989x434&quality=96&proxy=1&sign=db4f7080fcfb31c0e94e45f74a10b3b2&type=album)  
Понравившиеся собаки попадают в список лайков, не понравившиеся - в список дизлайков.  
На основе обратной связи пользователя делаются следующие рекомендации. Алгоритм - поиск на основе массива с учетом дизлайков из лр 4.  
![alt text](https://sun9-32.userapi.com/impf/3foIe39gHdLHBo4TOagEnfajCcORCQ_8muz1nA/iA87OnfN8gw.jpg?size=993x443&quality=96&proxy=1&sign=270b87eb7ee45f568a7eab95b65a1006&type=album)  
Теперь пользователь может оценить следующие рекомендации и т. д., пока есть, что предлагать.
