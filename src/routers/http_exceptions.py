from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found",
)
