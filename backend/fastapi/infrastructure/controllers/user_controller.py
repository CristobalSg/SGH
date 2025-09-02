from fastapi import APIRouter, HTTPException, status
from domain.entities import UserLogin
from application.use_cases import CreateUserUseCase, LoginUseCase
from infrastructure.repositories.user_repository_memory import UserRepositoryInMemory

router = APIRouter(prefix="/users", tags=["users"])
user_repository = UserRepositoryInMemory()

@router.post("/register")
def register_user(username: str, password: str, email: str):
    use_case = CreateUserUseCase(repo=user_repository)
    try:
        user = use_case.execute(username=username, password=password, email=email)
        return {"message": "Usuario creado exitosamente", "user_id": str(user.id)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
def login(login_data: UserLogin):
    use_case = LoginUseCase(repo=user_repository)
    user = use_case.execute(login_data)
    if user:
        return {
            "message": "Login exitoso",
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas"
    )
