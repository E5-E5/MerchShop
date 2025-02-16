from fastapi import APIRouter, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.service.implementation.StorageService import StorageService
from src.dto.api import ErrorResponse
from src.service.jwt.JWTAuth import JWTService
from src.initialization import get_storage_service, get_jwt_service

router = APIRouter()
security = HTTPBearer()


@router.get("/api/buy/{item}", responses={
    200: {"description": "Успешный ответ"},
    400: {"model": ErrorResponse, "description": "Неверный запрос"},
    401: {"model": ErrorResponse, "description": "Неавторизован"},
    500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
})
def buy_item(
        item: str,
        credentials: HTTPAuthorizationCredentials = Security(security),
        storage_service: StorageService = Depends(get_storage_service),
        jwt_service: JWTService = Depends(get_jwt_service)
):
    token = credentials.credentials

    user_id = jwt_service.validate_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Неверный токен")

    try:
        storage_service.add_to_storage(user_id, item)
        return {"message": f"Предмет '{item}' успешно куплен"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
