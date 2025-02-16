from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.service.implementation.UserService import UserService, UserServiceI
from src.service.implementation.StorageService import StorageService, StorageServiceI
from src.service.implementation.ExchangeService import ExchangeService, ExchangeServiceI

from src.storage.connector.PGConnector import PostgresDBConnector
from src.dto.api import InfoResponse, ErrorResponse
from src.initialization import get_user_service, get_exchange_service, get_storage_service

router = APIRouter()
security = HTTPBearer()


# connector = PostgresDBConnector()
# user_service: UserServiceI = UserService(connector)  # Экземпляр сервиса
# storage_service: StorageService = StorageService(connector)  # Экземпляр сервиса
# exchange_service: ExchangeServiceI = ExchangeService(connector)  # Экземпляр сервиса


@router.get("/api/info", response_model=InfoResponse, responses={
    400: {"model": ErrorResponse, "description": "Неверный запрос"},
    401: {"model": ErrorResponse, "description": "Неавторизован"},
    500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
})
def get_user_info(credentials: HTTPAuthorizationCredentials = Security(security),
                  user_service: UserService = Depends(get_user_service),
                  storage_service: StorageService = Depends(get_storage_service),
                  exchange_service: ExchangeService = Depends(get_exchange_service)):
    token = credentials.credentials
    user_id = user_service.jwt.validate_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Неверный токен")

    try:
        coins = user_service.get_user_coin(user_id)
        storage = storage_service.get_list_of_storage(user_id)
        history = exchange_service.get_coin_history(user_id)

        return InfoResponse(
            coins=coins,
            inventory=storage,
            coinHistory=history
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
