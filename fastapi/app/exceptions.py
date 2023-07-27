from fastapi import HTTPException, status

UserHasNoPrivileges = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="У вас недостаточно прав"
)

UserAlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует"
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверная почта или пароль"
)

TokenExpireException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истек"
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен отсутствует"
)

IncorrectTokenFormanException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный формат токена"
)

UserIsNotPresentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED
)