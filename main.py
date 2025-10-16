from db.db import db
import asyncio
import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

async def test_async_connection():
    """Prueba conexión asíncrona con consulta raw"""
    try:
        # Crear engine asíncrono
        database_url = os.getenv("DATABASE_URL")
        print(f"Conectando a: {database_url}")
        
        engine = create_async_engine(
            database_url,
            echo=True,  # Ver las consultas SQL en consola
            pool_pre_ping=True  # Verificar conexión antes de usar
        )
        
        # Crear sesión
        async_session = sessionmaker(
            engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )
        
        async with async_session() as session:
            # Consulta de prueba - información del servidor
            result = await session.execute(
                text("SELECT @@VERSION as version, @@SERVERNAME as server_name, DB_NAME() as database_name")
            )
            
            row = result.fetchone()
            print("\n🟢 CONEXIÓN EXITOSA!")
            print(f"Servidor: {row.server_name}")
            print(f"Base de datos: {row.database_name}")
            print(f"Versión: {row.version[:50]}...")
            
            # Consulta a las tablas de tu sistema
            tables_result = await session.execute(
                text("""
                    SELECT 
                        TABLE_SCHEMA,
                        TABLE_NAME,
                        TABLE_TYPE
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE = 'BASE TABLE'
                    ORDER BY TABLE_SCHEMA, TABLE_NAME
                """)
            )
            
            print("\n📋 TABLAS DISPONIBLES:")
            for table in tables_result.fetchall():
                print(f"  - {table.TABLE_SCHEMA}.{table.TABLE_NAME}")
        
        await engine.dispose()
        
    except Exception as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")
        print(f"Tipo de error: {type(e).__name__}")


asyncio.run(test_async_connection()) 