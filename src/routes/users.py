from fastapi import APIRouter, HTTPException, status

from src.models.user import User
from src.utils.logger import logger
from src.models.appointment import Appointment
from src.db.collections.users import UsersCollection

users_router = APIRouter(prefix='/users')
users_collection = UsersCollection

@users_router.get('')
async def get_all_users() -> list[User]:
    try:
        logger.info('Getting all users')
        users = await UsersCollection().find({})
        return users
    except Exception as e:
        logger.error(f'Error while getting all users: {e}')
        raise e

@users_router.post('', status_code=status.HTTP_201_CREATED)
async def post_users(users: list[User]) -> list[str]:
    try:
        logger.info('Inserting new users')
        return await UsersCollection().insert_many(users)
    except Exception as e:
        logger.error(f'Error while inserting users: {e}')
        raise e
    
@users_router.get('/{id}')
async def get_user_by_id(id: str) -> User:
    try:
        logger.info(f"Getting a user by id: {id}")
        user = await UsersCollection().find_one({"_id": id})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Cannot find user with id {id}'
            )
        return user
    except Exception as e:
        logger.error(f'Error while getting a user by id: {e}')
        raise e
    
@users_router.put('/{id}/appointment')
async def add_appointment_to_user(id: str, appointment: Appointment) -> User:
    try:
        logger.info(f'Adding new appointment to user with id {id}')
        result = await UsersCollection().update_one(
            {"_id": id}, 
            {"$addToSet": {"appointments": appointment.model_dump()}},
        )
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Cannot find user with id {id}'
            )
        return result
    except Exception as e:
        logger.error(f'Error while adding new appointment to user: {e}')
        raise e
