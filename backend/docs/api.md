# API Documentation

## Base Specification

- **Protocol**: HTTP / HTTPS
- **Format**: JSON (`application/json`)
- **API Versioning**: URL Path Versioning (`/api/v1`)
- **Swagger Interactive Documentation**: `/docs`
- **ReDoc Interactive Documentation**: `/redoc`

## Base Endpoints

### 1. Root Information
- **URL**: `/`
- **Method**: `GET`
- **Response**:
```json
{
  "message": "Welcome to AI Resume Analyzer API",
  "docs": "/docs",
  "api_v1": "/api/v1"
}
```

### 2. System Health Check
- **URL**: `/api/v1/health`
- **Method**: `GET`
- **Response**:
```json
{
  "status": "healthy",
  "version": "v1"
}
```
