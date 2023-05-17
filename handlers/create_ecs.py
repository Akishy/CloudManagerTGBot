from aiogram import types, Dispatcher
from data.config import dispatcher
import logging

# Import Cloud API Functions
from cloud.iam_management.get_project_id import get_project_id
from cloud.image_management.list_images import get_list_images
from cloud.vpc_managment.list_virtual_private_cloud import list_virtual_private_cloud
from cloud.ecs_management.flavour_management.get_list_flavours import get_list_flavours
from cloud.ecs_management.az_management.get_list_availability_zones import get_list_availability_zones
from cloud.vpc_managment.vpc_subnets_configuration.get_list_vpc_subnets import get_list_vpc_subnets

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from cloud.ecs_management.ecs_create_server import ecs_create_server

from utils.db_api import db_commands as cmd
from utils.db_api import db_gino

from aiogram.dispatcher import FSMContext
from states.ecs_state import Create_ECS

from keyboards.client_keyboards import gen_markup


# ----- Configurating logs ----- #
logging.basicConfig(filename="logs/logs.txt", filemode='w', level=logging.INFO)


# ----- /create_ecs ----- #
# @dispatcher.message_handler(text=['💻 Создать ECS 💻'])
# ----- State: token ----- #
async def ecs_create_start(message: types.Message):
	# Перехватываем ответ и переносим в следующий хэндлер для обратотки
	await Create_ECS.next()

	# Выводим сообщение
	await message.answer('Начинаем процесс создания!', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Ok", callback_data=f"Ok")))


async def set_token_state(callback_query: types.CallbackQuery, state: FSMContext):
	# Вытаскиваем токен относительно id пользователя телеграмма (БД)
	async with state.proxy() as data:
		data['token'] = await cmd.select_token(callback_query.from_user.id)

		# Переходим в следущий state и задаем вопрос
		await Create_ECS.next()

		# Получаем информацию о проектах
		dict_projects = get_project_id(data['token'])

		# Выделяем списки для передачи в функцию создания Inline-клавиатуры
		projects_name = list(dict_projects.keys())
		projects_id = list(dict_projects.values())
		
		# Отправляем пользователю сооьщение кнопки с проектами
		await callback_query.message.answer(text='💼 Вывожу список твоих проектов! Для того, чтобы продолжить, выбери, где необходимо создать ECS 💼', parse_mode="html", reply_markup=gen_markup(projects_name, projects_id, 2))
		await callback_query.answer()


async def set_project_id_state(callback_query: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['project_id'] = callback_query.data

		# Переходим в следущий state и задаем вопрос
		await Create_ECS.next()

		# Получаем информацию об образах
		dict_images = get_list_images(data['token'])

		# Выделяем списки для передачи в функцию создания Inline-клавиатуры
		images_name = list()
		images_id = list()

		for i in range(len(dict_images.images)):
			images_id.append(str(dict_images.images[i].id))
			images_name.append(dict_images.images[i].name)

		# Основная строка сообщения
		images_info = "Вывожу список доступных образов для последующей установки на ECS:\n"

		# Динамическая генерация списка с образами
		for i in range(len(images_name)):
			images_info = images_info + f"\t\t\t\t<b>├─</b> {images_name[i]}\n"

		await callback_query.message.answer(f"Теперь выбираем образ ВМ ECS!\n" + images_info, parse_mode="html", reply_markup=gen_markup(images_name, images_id, 2))
		await callback_query.answer()


async def set_ik_image_ref(callback_query: types.CallbackQuery, state: FSMContext):
	# Вытаскиваем токен относительно id пользователя телеграма
	async with state.proxy() as data:
		data['image_ref'] = callback_query.data

		# Переходим в следущий state и задаем вопрос
		await Create_ECS.next()

		# Получаем доступные зоны при применении соответствующей функции
		# az = get_list_availability_zones(data['token'], data['project_id'])

		await callback_query.message.answer("Образ выбран, определемся с зоной размещения ВМ", reply_markup=InlineKeyboardMarkup().add(
			InlineKeyboardButton(text="ru-moscow-1a", callback_data=f"ru-moscow-1a"),
			InlineKeyboardButton(text="ru-moscow-1b", callback_data=f"ru-moscow-1b"),
			InlineKeyboardButton(text="ru-moscow-1b", callback_data=f"ru-moscow-1b")
		))
		await callback_query.answer()


async def set_ik_az(callback_query: types.CallbackQuery, state: FSMContext):
	# Вытаскиваем токен относительно id пользователя телеграма
	async with state.proxy() as data:
		data['az'] = callback_query.data

		# Переходим в следущий state и задаем вопрос
		await Create_ECS.next()

		# Получаем информацию об образах
		# dict_flavour = get_list_flavours(data['token'], data['project_id'], data['az'])
		# print(dict_flavour.flavors[0].id)

		await callback_query.message.answer("Зона размещения виртуальной машины выбрана! Теперь выберем конфигурацию", reply_markup=InlineKeyboardMarkup().add(
			InlineKeyboardButton(text="1 vCPUs | 2 GiB", callback_data=f"s7n.medium.2"),
			InlineKeyboardButton(text="1 vCPUs | 4 GiB", callback_data=f"s7n.medium.4"),
			InlineKeyboardButton(text="1 vCPUs | 4 GiB", callback_data=f"s6.medium.4"),
		))
		await callback_query.answer()


async def set_ik_flavour_ref(callback_query: types.CallbackQuery, state: FSMContext):
	# Вытаскиваем токен относительно id пользователя телеграма
	async with state.proxy() as data:
		data['flavour_ref'] = callback_query.data

		# Переходим в следущий state и задаем вопрос
		await Create_ECS.next()

		await callback_query.message.answer("Конфигурация установлена, самое время выбрать имя для ECS!", reply_markup=InlineKeyboardMarkup().add(
			InlineKeyboardButton(text="Ubuntu x64", callback_data="Ubuntu"),
			InlineKeyboardButton(text="Ubuntu-Server", callback_data="Ubuntu-Server"),
			InlineKeyboardButton(text="x64-Ubuntu-Server", callback_data="x64-Ubuntu-Server"),
		))

		await callback_query.answer()


async def set_ik_name(callback_query: types.CallbackQuery, state: FSMContext):
	# Вытаскиваем токен относительно id пользователя телеграма
	async with state.proxy() as data:
		data['name'] = callback_query.data
		
		# Переходим в следущий state и задаем вопрос
		await Create_ECS.next()

		vpc_list = list_virtual_private_cloud(data["token"], data["project_id"])

		await callback_query.message.answer("Имя выбрано, переходим к VPC", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=f"{vpc_list.vpcs[0].name}", callback_data=f"{vpc_list.vpcs[0].id}")))
		await callback_query.answer()


async def set_ik_vpcid(callback_query: types.CallbackQuery, state: FSMContext):
	# Вытаскиваем токен относительно id пользователя телеграма
	async with state.proxy() as data:
		data['vpcid'] = callback_query.data

		# Переходим в следущий state и задаем вопрос
		await Create_ECS.next()
		
		subnets_list = get_list_vpc_subnets(data["token"], data["project_id"], data["vpcid"])

		await callback_query.message.answer("VPC выбран, выбираем Subnet", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=f"{subnets_list.subnets[0].name}", callback_data=f"{str(subnets_list.subnets[0].id)}")))
		await callback_query.answer()


async def set_ik_subnet_id(callback_query: types.CallbackQuery, state: FSMContext):
	# Вытаскиваем токен относительно id пользователя телеграма
	async with state.proxy() as data:
		data['subnet_id'] = callback_query.data

		# Переходим в следущий state и задаем вопрос
		await Create_ECS.next()

		await callback_query.message.answer("Subnet установлен, установим тип диска", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="SSD", callback_data="SSD")))
		await callback_query.answer()


async def set_ik_volumetype(callback_query: types.CallbackQuery, state: FSMContext):
	# Вытаскиваем токен относительно id пользователя телеграма
	async with state.proxy() as data:
		data['volumetype'] = callback_query.data

		# Переходим в следущий state и задаем вопрос
		await Create_ECS.next()

		await callback_query.message.answer("Тип диска мы выбрали, осталось выбрать, сколько памяти выделить", reply_markup=InlineKeyboardMarkup().add(
			InlineKeyboardButton(text="60", callback_data="60"),
			InlineKeyboardButton(text="80", callback_data="80"),
			InlineKeyboardButton(text="100", callback_data="100"),
			InlineKeyboardButton(text="120", callback_data="120"),
			InlineKeyboardButton(text="150", callback_data="150")
		))
		await callback_query.answer()


async def set_ik_disc_size(callback_query: types.CallbackQuery, state: FSMContext):
	# Вытаскиваем токен относительно id пользователя телеграма
	async with state.proxy() as data:
		data['disc_size'] = callback_query.data

		# Переходим в следущий state и задаем вопрос
		await Create_ECS.next()

		await callback_query.message.answer(f"На этом все! Отправляю запрос на создание ECS в системе Cloud!\n", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Подтвердить", callback_data="Подтвердить")))
		await callback_query.answer()


async def create_ecs(callback_query: types.CallbackQuery, state: FSMContext):
	# Вытаскиваем токен относительно id пользователя телеграма
	async with state.proxy() as data:
		data['check'] = callback_query.data

		# Переходим в следущий state и задаем вопрос
		await Create_ECS.next()

		ecs = ecs_create_server(
			data["token"],
			data["project_id"],
			data["image_ref"],
			data["flavour_ref"],
			data["name"],
			data["vpcid"],
			data["subnet_id"],
			data["volumetype"],
			data["disc_size"]
		)

		await callback_query.message.answer("Машина создается!")
		await callback_query.answer()
		await state.finish()



def register_handlers(dp: Dispatcher):
	dp.register_message_handler(ecs_create_start, text=['💻 Создать ECS 💻'])
	dp.register_callback_query_handler(set_token_state, state=Create_ECS.token)
	dp.register_callback_query_handler(set_project_id_state, state=Create_ECS.project_id)
	dp.register_callback_query_handler(set_ik_image_ref, state=Create_ECS.image_ref)
	dp.register_callback_query_handler(set_ik_az, state=Create_ECS.az)
	dp.register_callback_query_handler(set_ik_flavour_ref, state=Create_ECS.flavour_ref)
	dp.register_callback_query_handler(set_ik_name, state=Create_ECS.name)
	dp.register_callback_query_handler(set_ik_vpcid, state=Create_ECS.vpcid) 
	dp.register_callback_query_handler(set_ik_subnet_id, state=Create_ECS.subnet_id)
	dp.register_callback_query_handler(set_ik_volumetype, state=Create_ECS.volumetype)
	dp.register_callback_query_handler(set_ik_disc_size, state=Create_ECS.disc_size)
	dp.register_callback_query_handler(create_ecs, state=Create_ECS)
