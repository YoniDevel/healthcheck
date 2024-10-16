import logging
from fastapi import APIRouter, HTTPException, status
import pymongo
import pymongo.errors
from src.models.user import User
from src.db.collections.users import UsersCollection

users_router = APIRouter(prefix='/users')
users_collection = UsersCollection

@users_router.get('')
async def get_all_users() -> list[User]:
    try:
        logging.info('Getting all users')
        users = await UsersCollection().find({})
        return users
    except HTTPException as e:
        logging.error(f'Error while getting all users - http error: {e}')
        raise e
    except pymongo.errors.PyMongoError as e:
        logging.error(f'Error while getting all users - mongo error: {e}')
        raise e

@users_router.post('', status_code=status.HTTP_201_CREATED)
async def post_users(users: list[User]) -> list[str]:
    try:
        logging.info('Inserting new users')
        return await UsersCollection().insert_many(users)
    except Exception as e:
        logging.error(f'Error while inserting users: {e}')
        raise HTTPException(500, e)
