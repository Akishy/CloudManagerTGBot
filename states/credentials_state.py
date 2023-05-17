from aiogram.dispatcher.filters.state import StatesGroup, State


# ----- State User Credentials Class ----- #
class User_IAM_Credentials(StatesGroup):
	iam_user_name = State() 	 # IAM User Name
	iam_account_name = State()   # IAM User ID (domain)
	iam_password = State()		 # Password