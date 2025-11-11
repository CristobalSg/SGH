#!/usr/bin/env python3
"""
Script para listar las credenciales de usuarios de desarrollo.

Uso:
    python scripts/show_dev_credentials.py
"""

import os
import sys
from pathlib import Path

# Ajustar el PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import settings

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_credentials():
    """Muestra las credenciales de desarrollo de forma clara."""
    
    print(f"\n{Colors.BLUE}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}        CREDENCIALES DE USUARIOS DE DESARROLLO - SGH{Colors.ENDC}")
    print(f"{Colors.BLUE}{'='*70}{Colors.ENDC}\n")
    
    # Administrador
    print(f"{Colors.GREEN}{Colors.BOLD}👨‍💼 ADMINISTRADOR{Colors.ENDC}")
    print(f"  {Colors.CYAN}Nombre:{Colors.ENDC}     {settings.initial_admin_name or 'NO CONFIGURADO'}")
    print(f"  {Colors.CYAN}Email:{Colors.ENDC}      {settings.initial_admin_email or 'NO CONFIGURADO'}")
    print(f"  {Colors.CYAN}Password:{Colors.ENDC}   {settings.initial_admin_password or 'NO CONFIGURADO'}")
    print()
    
    # Docente
    print(f"{Colors.GREEN}{Colors.BOLD}👨‍🏫 DOCENTE{Colors.ENDC}")
    if settings.dev_docente_email:
        print(f"  {Colors.CYAN}Nombre:{Colors.ENDC}        {settings.dev_docente_name}")
        print(f"  {Colors.CYAN}Email:{Colors.ENDC}         {settings.dev_docente_email}")
        print(f"  {Colors.CYAN}Password:{Colors.ENDC}      {settings.dev_docente_password}")
        print(f"  {Colors.CYAN}Departamento:{Colors.ENDC}  {settings.dev_docente_departamento}")
    else:
        print(f"  {Colors.WARNING}No configurado (define DEV_DOCENTE_* en .env.development){Colors.ENDC}")
    print()
    
    # Estudiante
    print(f"{Colors.GREEN}{Colors.BOLD}👨‍🎓 ESTUDIANTE{Colors.ENDC}")
    if settings.dev_estudiante_email:
        print(f"  {Colors.CYAN}Nombre:{Colors.ENDC}      {settings.dev_estudiante_name}")
        print(f"  {Colors.CYAN}Email:{Colors.ENDC}       {settings.dev_estudiante_email}")
        print(f"  {Colors.CYAN}Password:{Colors.ENDC}    {settings.dev_estudiante_password}")
        print(f"  {Colors.CYAN}Matrícula:{Colors.ENDC}   {settings.dev_estudiante_matricula}")
    else:
        print(f"  {Colors.WARNING}No configurado (define DEV_ESTUDIANTE_* en .env.development){Colors.ENDC}")
    print()
    
    # Advertencias
    print(f"{Colors.BLUE}{'─'*70}{Colors.ENDC}")
    print(f"{Colors.WARNING}{Colors.BOLD}⚠️  ADVERTENCIAS DE SEGURIDAD:{Colors.ENDC}")
    print(f"{Colors.WARNING}   • Estas credenciales están en la BASE DE DATOS COMPARTIDA{Colors.ENDC}")
    print(f"{Colors.WARNING}   • Todos los miembros del equipo pueden ver estos usuarios{Colors.ENDC}")
    print(f"{Colors.WARNING}   • NO cambies las contraseñas sin coordinarlo con el equipo{Colors.ENDC}")
    print(f"{Colors.WARNING}   • En PRODUCCIÓN usa credenciales diferentes y seguras{Colors.ENDC}")
    print(f"{Colors.BLUE}{'='*70}{Colors.ENDC}\n")
    
    # Comandos útiles
    print(f"{Colors.CYAN}{Colors.BOLD}📝 Comandos Útiles:{Colors.ENDC}")
    print(f"  {Colors.CYAN}Crear/actualizar usuarios:{Colors.ENDC}")
    print(f"    docker compose --env-file .env.development exec backend python scripts/bootstrap_admin.py")
    print(f"    docker compose --env-file .env.development exec backend python scripts/bootstrap_dev_users.py")
    print()
    print(f"  {Colors.CYAN}Login con curl:{Colors.ENDC}")
    print(f"    curl -X POST http://localhost:8000/api/auth/login \\")
    print(f"      -H 'Content-Type: application/x-www-form-urlencoded' \\")
    print(f"      -d 'username={settings.initial_admin_email or 'admin@inf.uct.cl'}&password={settings.initial_admin_password or 'password'}'")
    print(f"\n{Colors.BLUE}{'─'*70}{Colors.ENDC}\n")


if __name__ == "__main__":
    try:
        print_credentials()
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {str(e)}{Colors.ENDC}\n")
        print(f"{Colors.WARNING}Asegúrate de haber cargado las variables de entorno:{Colors.ENDC}")
        print(f"  export $(cat .env.development | xargs)\n")
        sys.exit(1)
