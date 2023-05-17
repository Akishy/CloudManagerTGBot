from aiogram.dispatcher.filters.state import StatesGroup, State


# ECS State (for creating)
class Create_ECS(StatesGroup):
	token = State()
	project_id = State()
	image_ref = State()
	az = State()
	flavour_ref = State()
	name = State()
	vpcid = State()
	subnet_id = State()
	volumetype = State()
	disc_size = State()
	check = State()