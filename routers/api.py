from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from src.data.scripts.connection import get_connection

router = APIRouter(prefix="/api", tags=["api"])

# Modelos
class Project(BaseModel):
    id: int
    name: str

class Device(BaseModel):
    id: int
    project_id: int
    mean_delta: float
    std_delta: float
    var_delta: float

class AuditData(BaseModel):
    id: str
    device_id: int
    delta_value: float
    accumulated_value: float
    clasificacion: Optional[str]
    timestamp: str

class ValidRecord(BaseModel):
    id: str
    device_id: int
    delta_value: float
    accumulated_value: float
    timestamp: str

# Endpoints de Projects
@router.get("/projects", response_model=List[Project])
def read_projects():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM projects")
        rows = cursor.fetchall()
    finally:
        conn.close()
    return [Project(id=r[0], name=r[1]) for r in rows]

@router.get("/projects/{project_id}", response_model=Project)
def read_project(project_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(404, "Proyecto no encontrado")
    finally:
        conn.close()
    return Project(id=row[0], name=row[1])

# Endpoints de Devices
# Listar dispositivos (opcionalmente filtrados)
@router.get("/devices", response_model=List[Device])
def read_devices(project_id: int = None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = "SELECT id, project_id, mean_delta, std_delta, var_delta FROM devices"
        params = ()
        if project_id is not None:
            sql += " WHERE project_id = ?"
            params = (project_id,)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    finally:
        conn.close()
    return [
        Device(id=r[0], project_id=r[1], mean_delta=r[2], std_delta=r[3], var_delta=r[4])
        for r in rows
    ]



# Endpoint de AuditData
@router.get("/audit_data", response_model=List[AuditData])
def read_audit_data(device_id: Optional[int] = None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = (
            "SELECT id, device_id, delta_value, accumulated_value, clasificacion, timestamp "
            "FROM audit_data"
        )
        params = ()
        if device_id is not None:
            sql += " WHERE device_id = ?"
            params = (device_id,)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    finally:
        conn.close()
    return [
        AuditData(
            id=r[0],
            device_id=r[1],
            delta_value=r[2],
            accumulated_value=r[3],
            clasificacion=r[4],
            timestamp=r[5]
        ) for r in rows
    ]

# Endpoint de ValidRecords
@router.get("/valid_records", response_model=List[ValidRecord])
def read_valid_records(device_id: Optional[int] = None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = (
            "SELECT id, device_id, delta_value, accumulated_value, timestamp "
            "FROM valid_records"
        )
        params = ()
        if device_id is not None:
            sql += " WHERE device_id = ?"
            params = (device_id,)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    finally:
        conn.close()
    return [
        ValidRecord(
            id=r[0],
            device_id=r[1],
            delta_value=r[2],
            accumulated_value=r[3],
            timestamp=r[4]
        ) for r in rows
    ]


