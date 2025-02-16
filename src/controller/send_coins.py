from fastapi import APIRouter, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.service.implementation.ExchangeService import ExchangeService
from src.service.interface.ExchangeServiceI import ExchangeServiceI
from src.storage.connector.PGConnector import PostgresDBConnector
from src.service.jwt.JWTAuth import JWTService
from src.dto.api import SendCoinRequest, ErrorResponse
from src.initialization import get_exchange_service, get_jwt_service

router = APIRouter()
security = HTTPBearer()


# connector = PostgresDBConnector()
# exchange_service: ExchangeServiceI = ExchangeService(connector)

@router.post("/api/sendCoin", responses={
    200: {"description": "Успешный ответ"},
    400: {"model": ErrorResponse, "description": "Неверный запрос"},
    401: {"model": ErrorResponse, "description": "Неавторизован"},
    500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
})
def send_coin(
        request: SendCoinRequest,
        credentials: HTTPAuthorizationCredentials = Security(security),
        exchange_service: ExchangeService = Depends(get_exchange_service),
        jwt_service: JWTService = Depends(get_jwt_service)
):
    token = credentials.credentials
    sender_id = jwt_service.validate_token(token)

    if not sender_id:
        raise HTTPException(status_code=401, detail="Неверный токен")

    try:
        exchange_service.give_coins(sender_id, request.toUser, request.amount)
        return {"message": "Монеты успешно отправлены"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
