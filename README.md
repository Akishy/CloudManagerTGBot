<p align="center">
    <img src="URL">
</p>

<h1 align="center">
Cloud Management - Telegram Bot
</h1>

<p align="justify">&emsp;&emsp;Данный репозиторий включает в себя реализацию кейса по разработке Telegram бота, который позволяет управлять облаком (Cloud) с хакатона "киб_хак" (11.05.2023 - 18.05.2023).</p>

<h1 align="center">
Задача от Cloud: разработать телеграм-бота для управления облаком
</h1>

<h3 align="center">
    Вводная часть
</h3> 

<p align="justify">&emsp;&emsp;Разработать телеграм-бота для работы с облаком Cloud Advanced — создание виртуальных машин, баз данных, дисков, других сервисов и управление ими.</p>

<p align="justify">&emsp;&emsp;Для реализации нужно поработать с API облака, вот ссылки на документацию от Cloud (https://cloud.ru/ru/docs/advanced.html) и документацию от Huawei Cloud (https://developer.huaweicloud.com/intl/en-us/openapilist).</p>


<h3 align="center">
    Функциональные требования
</h3> 

&emsp;&emsp;:white_check_mark: Можно создавать, редактировать, удалять как минимум пять типов ресурсов.

&emsp;&emsp;:white_check_mark: Можно получать информацию о доступных конфигурациях ресуров.

&emsp;&emsp;:white_check_mark: Выгрузка отчёта по всем потребляемым ресурсам.

&emsp;&emsp;:white_check_mark: Возможность получить сгенерированный терраформ-код для ресурса вместо создания.

&emsp;&emsp;:white_check_mark: Есть мониторинг ресурса.

<h3 align="center">
    Нефункциональные требования
</h3> 

&emsp;&emsp;:white_check_mark: Использован SDK (https://github.com/huaweicloud/huaweicloud-sdk-python-v3).

&emsp;&emsp;:white_check_mark: Авторизация с возможностью контроля прав доступа и грамотная обработка отсутствия у бота прав.

&emsp;&emsp;:white_check_mark: Несложно добавить поддержку нового сервиса.

&emsp;&emsp;:white_check_mark: Код покрыт тестами.

<h3 align="center">
    Критерии оценки
</h3> 

<p align="justify">&emsp;&emsp;Выполнять все требования необязательно, но с выполнением повышается шанс на победу. Учитывается:</p>
&emsp;&emsp;:white_check_mark: Качество основного функционала — должны быть реализованы минимальные требования к разрабатываемому программному решению.

&emsp;&emsp;:white_check_mark: Количество и качество реализации дополнительного функционала.

&emsp;&emsp;:white_check_mark: Качество презентации и родмапа — функционал может быть готов не до конца, но хорошо продуман и обоснован, тогда о нём можно рассказать. Всегда есть 4. пространство для манёвра.

&emsp;&emsp;:white_check_mark: Грамотность программного кода и архитектуры.

&emsp;&emsp;:white_check_mark: Удобство UX.

<h2 align="center">
    Описание решения
</h2>

&emsp;&emsp;:red_circle: 1.  Для работы с платформой была реализована библиотека с пакетами python, которая позволяет **полностью оперировать запросами на сервер** (например, для оперирования жизненным циклом сервиса Elastic Cloud Server (виртуальные машины), что представлено в данном проекте)

&emsp;&emsp;:red_circle: 2.  Один из главных аспектов кейса - Telegram бот, олицетворяющий интерфейс и удобное диалоговое окно для управления. В боте реализован полный цикл общения с клиентом - от авторизации до создания виртуальной машины. В ходе создания машины бот предоставляет возможность выбора машин по запросу клиента (реализована система фильтрации запроса на сервер).

&emsp;&emsp;:red_circle: 3.  Для удобства в навигации внедрена клавиатура с необходимыми кнопками, адаптирующая общение с ботом.

&emsp;&emsp;:red_circle: 4.  Познакомиться с ботом и командой подробнее можно нажав по кнопке *"Info"* и по [ссылке](https://akishy.github.io) 


<h3 align="center">
    Cледующая таблица описывает поведение той или иной функции, внедренной в бота через пакеты python
</h3>

| Папка                            | Краткое описание папки                                                                                                                                                                                                                                                                        | Пакет                          | Функции в пакете                                                                 | описание функции                                                                                                                                                                                                                                                                       |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ecs_management                   | В данной папке находятся пакеты  для реализации Elastic Cloud Server. В ней находятся такие папки как az_management,  ecs_group_management, flavour_management.                                                                                                                               | ---                            | ---                                                                              | ---                                                                                                                                                                                                                                                                                    |
| ecs_management                   |                                                                                                                                                                                                                                                                                               | ecs_create_server              | x_auth, project_id, image_ref,  flavour_ref, name, vpcid, subnet_id, volumetype) | Функция принимает восемь значений для создания сервера. Токен, id проекта, iso образ, референс машины,  id сети ,id подсети, тип диска для системы, размер диска. Возвращает тех информацию о созданном сервере.                                                                       |
| az_management                    | Данная папка располагает пакетами для работы с  Active Zones. Это помогает клиенту определиться с физическим расположением будущей машины.                                                                                                                                                    | get_list_availability_zones.py | get_list_availability_zones(x_auth:  str ,  project_id:  str)                    | функция принимает два обязательных значения: токен авторизации и ID проекта. Функция возвращает динамически сгенерированный объект с параметрами о всех AZ, в том числе имя, доступные хосты в каждой зоне и  статус зоны (активна/неактивна).                                         |
| ecs_group_management             | Данная папка раполагает пакетами для работы с группами ECS. Это необходимо для служебной информации для работы бота, а так же предоставляет возможность выбора проекта для пользователя.                                                                                                      | list_server_groups.py          | list_server_groups(x_auth, project_id)                                           | Функция принимает два обязательных значения: токен авториации и ID проекта. Функция  возвращает список доступных групп, а так же описание каждой группы (id, имя, метаданные, участники, политики).                                                                                    |
| flavour_management               | Данная папка располагает пакетами для работы и выбора конфигурации будущего сервера.                                                                                                                                                                                                          | get_list_flavours.py           | get_list_flavours (x_auth, project_id, availability_zone)                        | Функция принимает три обязательных значения: токен авторизации и ID проекта. Возвращает динамически  сгенерированный объект с необходимой информацией по каждой конфигурации.                                                                                                          |
| iam_management                   | Данная папка располагает пакетами для работы с идентификацией и доступом. В ней находятся пакеты для создания временных ключей, получения информации об аккаунте,  id домена, id проекта, получения токена пользователя и его валидации                                                       | ---                            | ---                                                                              | ---                                                                                                                                                                                                                                                                                    |
| iam_management                   |                                                                                                                                                                                                                                                                                               | create_temporary_access_key.py | create_temporary_access_key (iam_token, time_to_live_sec)                        | принимает два обязательных значения: токен и время жизни будущего ключа доступа. Возвращает информацию о созданном ключе доступа: Access key, Secret Key, securitytoken.                                                                                                               |
| iam_management                   |                                                                                                                                                                                                                                                                                               | get_account_info.py            | get_account_info(auth_token)                                                     | возвращает словарь, в котором информация об аккаунте в таком порядке: ключ[имя аккаунта] = значение[id_аккаунта]                                                                                                                                                                       |
| iam_management                   |                                                                                                                                                                                                                                                                                               | get_domain_id.py               | get_domain_id(auth_token)                                                        | принимает токен авторизации. Возвращает все домены с их информацией (состояние, id, имя, описание).                                                                                                                                                                                    |
| iam_management                   |                                                                                                                                                                                                                                                                                               | get_project_id.py              | get_project_id.py(auth_token)                                                    | принимает токен авторизации. Возвращает словарь со всеми проектами, который хранит ключ{имя проекта}: значение {id проекта}                                                                                                                                                            |
| iam_management                   |                                                                                                                                                                                                                                                                                               | get_user_token.py              | get_user_token(user_name, domain_name, passw)                                    | принимает три значения: имя пользователя, имя домена, пароль. Возвращает токен авторизации.                                                                                                                                                                                            |
| iam_management                   |                                                                                                                                                                                                                                                                                               | validate_token.py              | validate_token(x_auth_verification_token,  x_subject_token_to_validate)          | Функция принимает 2 значения: токен администратора; токен, который хочешь проверить на валидность. (Можно проверить токен администратора, если ввести в оба поля один и тот же токен). Возвращает объект класса Token, в котором полная информация о токене, его владельце, эндпойнтах |
| region_configuration             | Данная папка используется для конфигурации региона. В ней находятся описания классов для работы с сайтом, определены классы пользователя, региона, и другой технической информации.                                                                                                           | region_config.py               | ---                                                                              | пакет импортируется в другие пакеты для получения технической информации.                                                                                                                                                                                                              |
| virtual_private_cloud_management | Данная папка располагает пакетами для работы с сетями и подсетями. Есть папка vpc_subnets_configuration.  Также располагает пакетами для работы с сетью.                                                                                                                                      | ---                            | ---                                                                              | ---                                                                                                                                                                                                                                                                                    |
| virtual_private_cloud_management |                                                                                                                                                                                                                                                                                               | list_virtual-private_cloud     | list_virtual_private_cloud (iam_token:  str ,  project_id:  str)                 | Функция принимает 2 значения: IAM_token, и project_id, который до этого был выбран пользователем в течение диалога с ботом  Функция возвращает класс VPC's, который содержит список с доступными сетями.                                                                               |
| handlers                         | В данной папке находятся пакеты для обработки сообщений ботом. Через хэндлеры пользователю доступна возможность конфигурирования системы, а так же реализована                                                                                                                                | ---                            | ---                                                                              | ---                                                                                                                                                                                                                                                                                    |
| keyboards                        | В данной папке сконфигурированы клавитатуры с кнопками, с помощью которых происходит инициализация той или иной команды бота.                                                                                                                                                                 | ---                            | ---                                                                              | ---                                                                                                                                                                                                                                                                                    |
| logs                             | Тут собраны файлы логов из бота. Техническая информация, которая использовалась при отладке.                                                                                                                                                                                                  | ---                            | ---                                                                              | ---                                                                                                                                                                                                                                                                                    |
| states                           | тут собраны файлы, управляющие стейтами. Стейты, в свою очередь, учавствуют в создании так называемого конечного автомата, представляя из себя некие шаги, следуя которым можно добиться конечного этапа (создания машины в облаке). После него процесс завершается и цикл начинается сначала | ---                            | ---                                                                              | ---                                                                                                                                                                                                                                                                                    |
| web                              | сайт, который позволяет более подробно ознакомиться с ботом и командой создателей.                                                                                                                                                                                                            | ---                            | ---                                                                              | ---                                                                                                                                                                                                                                                                                    |


<h3 align="center">
    Авторы
</h3>

Команда - **Impulse**:
<p align="justify">&emsp;&emsp;:red_circle: 1. Иорин Давид Андреевич (Team Leader)</p>
<p align="justify">&emsp;&emsp;:red_circle: 2. Богданов Данила Андреевич</p>
<p align="justify">&emsp;&emsp;:red_circle: 3. Беляев Иван Дмитриевич</p>
<p align="justify">&emsp;&emsp;:red_circle: 4. Малахов Арсений Константинович</p>
<p align="justify">&emsp;&emsp;:red_circle: 5. Морозов Андрей Александрович</p>