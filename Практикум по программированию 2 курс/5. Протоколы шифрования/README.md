При запуске клиент и сервер генерируют каждый свою пару ключей. При подключении клиент посылает серверу свой открытый ключ. В ответ, сервер посылает клиенту открытый ключ сервера. Клиент посылает сообщение серверу, шифруя его своим закрытым ключом и открытым ключом сервера. Сервер принимает сообщение, расшифровывает его сначала своим закрытым ключом, а потом - открытым ключом клиента. Обратное сообщение посылается аналогично. Для Шифровки - расшифровки используем фукнции симметричного шифрования из предыдущей работы по симметричному шифрованию по Unix

![image](https://user-images.githubusercontent.com/83708760/146561114-b47defe1-0cd9-434c-aaed-fbb9c9afe33a.png)

Далее в фукнции get_keys() читаем уже существующие ключи, если их нет создаются новые.

Модифицируйте код клиента и сервера так, чтобы приватный и публичный ключ хранились в текстовых файлах на диске и, таким образом, переиспользовались между запусками. Реализовано в коде, можно убедиться что между запусками ключи в файлах не меняются. csv файл с ключами клиента

![image](https://user-images.githubusercontent.com/90453727/144818613-5bdb7635-0034-476b-9c3a-a751960dac49.png)

csv файл с ключами сервера

![image](https://user-images.githubusercontent.com/90453727/144818676-bce27921-e7d1-4949-aa0b-ab6fe4d131d4.png)

Сервер хранит ключи для каждого из клиентов (по IP) Проведите рефакторинг кода клиента и сервера так, чтобы все, относящееся к генерации ключей, установлению режима шифрования, шифрованию исходящих и дешифрованию входящих сообщений было отделено от основного алгоритма обмена сообщениями.

Можно увидеть в коде
![image](https://user-images.githubusercontent.com/83708760/146561896-8d3be88f-1202-48b6-860c-9879f1adae1a.png)
![image](https://user-images.githubusercontent.com/83708760/146561954-72c22c1b-c29b-4d68-bd99-952e3d5f909e.png)
![image](https://user-images.githubusercontent.com/83708760/146562172-28aeb44f-3507-4630-895f-9e780c1b151b.png)


Реализуйте на сервере проверку входящих сертификатов. На сервере должен храниться список разрешенных ключей. Когда клиент посылает на сервер свой публичный ключ, сервер ищет его среди разрешенных и, если такого не находит, разрывает соединение. Проверьте правильность работы не нескольких разных клиентах. Важно! данный пункт предполагает, что ключи уже существуют, поэтому в репозитории приложены файлы с уже созданными ключами. Разрешенные открытые ключи клиентов хранятся в файле allowed.csv
![image](https://user-images.githubusercontent.com/90453727/144818954-0e164751-725a-4f8d-8bb0-c55b43877bd7.png)


Модифицируйте код клиента и сервера таким образом, чтобы установление режима шифрования происходило при подключении на один порт, а основное общение - на другом порту. Номер порта можно передавать как первое зашифрованное сообщение. Также можно увидеть в коде, и сервер и клиент выводят сообщени о подключении к конкретному порту. Изначально сервер подключился на порте 10101

![image](https://user-images.githubusercontent.com/90453727/144819041-9e1cc893-059d-48ea-b517-ac8dd3513d90.png)


После подключения клиента они переключились на новый (рандомный) порт и продолжают общение на нем
![image](https://user-images.githubusercontent.com/90453727/144819072-93306ee1-fe60-43c4-8790-a84737799a63.png)
![image](https://user-images.githubusercontent.com/90453727/144819149-f0ff662b-31c0-4ce0-b127-a7483aca2050.png)


Модифицируйте код FTP-сервера таким образом, чтобы он поддерживал шифрование.
ftp_client.py
![image](https://user-images.githubusercontent.com/83708760/146562492-83cc0f07-fd32-4f87-bf8e-4fbe3e8a3071.png)
ftp_server.py
![image](https://user-images.githubusercontent.com/83708760/146562569-6b226956-c5ec-47c3-bc58-2f0b39c9e736.png)


![image](https://user-images.githubusercontent.com/83708760/146562813-6389b893-9236-4218-b734-eab9e1413285.png)
![image](https://user-images.githubusercontent.com/83708760/146562867-605f95fa-e5e6-4cd6-b17d-ad982528eca4.png)
![image](https://user-images.githubusercontent.com/83708760/146563312-8966871d-5044-465a-a60e-462bb4fb2e8d.png)


методы send/recv заменены на собственно написанные s_send/s_recv которые поддерживают шифрование. Обмен ключами и генерация происходят при каждом запросе и каждый раз разные соответственно.

Запись всех действий в лог файл
![image](https://user-images.githubusercontent.com/83708760/146563461-e4e66a6f-4cf0-4c60-a117-c5ec376117e7.png)

