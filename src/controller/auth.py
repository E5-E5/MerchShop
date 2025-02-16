from fastapi import APIRouter, HTTPException, Depends
from src.service.implementation.UserService import UserService, UserServiceI
from src.dto.api import AuthRequest, AuthResponse, ErrorResponse
from src.storage.connector.PGConnector import PostgresDBConnector
from src.service.jwt.JWTAuth import JWTService
from src.initialization import get_user_service
from src.logger.Logger import Logger
from src.storage.implementation.UserStorage import UserStorage

router = APIRouter()


@router.post("/api/auth", response_model=AuthResponse, responses={
    200: {"description": "Успешная аутентификация"},
    400: {"model": ErrorResponse, "description": "Неверный запрос"},
    401: {"model": ErrorResponse, "description": "Неавторизован"},
    500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
})
def authenticate_user(auth_data: AuthRequest,
                      user_service: UserService = Depends(get_user_service)):
    try:
        token = user_service.authenticate_user(auth_data.username, auth_data.password)

        if not token:
            raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")

        return AuthResponse(token=token)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
