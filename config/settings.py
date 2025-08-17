"""
Configuration settings for the Ascend system.
"""

import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # LLM Configuration - Gemini
    GOOGLE_API_KEY: str = Field(default="your_google_api_key_here", env="GOOGLE_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-2.0-flash-lite", env="GEMINI_MODEL")
    GEMINI_TEMPERATURE: float = Field(default=0.7, env="GEMINI_TEMPERATURE")
    GEMINI_MAX_TOKENS: int = Field(default=4000, env="GEMINI_MAX_TOKENS")
    
    # Database Configuration - MongoDB
    MONGODB_CONNECTION_STRING: str = Field(default="mongodb://localhost:27017", env="MONGODB_CONNECTION_STRING")
    MONGODB_DATABASE_NAME: str = Field(default="ascend", env="MONGODB_DATABASE_NAME")
    
    # External Integrations
    GOOGLE_CALENDAR_API_KEY: Optional[str] = Field(default=None, env="GOOGLE_CALENDAR_API_KEY")
    GOOGLE_CALENDAR_ID: Optional[str] = Field(default=None, env="GOOGLE_CALENDAR_ID")
    
    # LMS Integration
    CANVAS_API_KEY: Optional[str] = Field(default=None, env="CANVAS_API_KEY")
    CANVAS_BASE_URL: Optional[str] = Field(default=None, env="CANVAS_BASE_URL")
    
    BLACKBOARD_API_KEY: Optional[str] = Field(default=None, env="BLACKBOARD_API_KEY")
    BLACKBOARD_BASE_URL: Optional[str] = Field(default=None, env="BLACKBOARD_BASE_URL")
    
    MOODLE_API_KEY: Optional[str] = Field(default=None, env="MOODLE_API_KEY")
    MOODLE_BASE_URL: Optional[str] = Field(default=None, env="MOODLE_BASE_URL")
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="logs/ascend.log", env="LOG_FILE")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    LOG_MAX_SIZE: str = Field(default="10MB", env="LOG_MAX_SIZE")
    LOG_BACKUP_COUNT: int = Field(default=5, env="LOG_BACKUP_COUNT")
    
    # System Configuration
    MAX_CONCURRENT_SESSIONS: int = Field(default=10, env="MAX_CONCURRENT_SESSIONS")
    SESSION_TIMEOUT: int = Field(default=3600, env="SESSION_TIMEOUT")
    SESSION_CLEANUP_INTERVAL: int = Field(default=300, env="SESSION_CLEANUP_INTERVAL")
    
    # Agent Configuration
    AGENT_TIMEOUT: int = Field(default=300, env="AGENT_TIMEOUT")
    AGENT_MAX_RETRIES: int = Field(default=3, env="AGENT_MAX_RETRIES")
    AGENT_RETRY_DELAY: int = Field(default=5, env="AGENT_RETRY_DELAY")
    
    # Workflow Configuration
    WORKFLOW_MAX_STEPS: int = Field(default=50, env="WORKFLOW_MAX_STEPS")
    WORKFLOW_TIMEOUT: int = Field(default=1800, env="WORKFLOW_TIMEOUT")
    
    # Security Configuration
    JWT_SECRET_KEY: str = Field(default="your-secret-key-change-this", env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_EXPIRATION_HOURS: int = Field(default=24, env="JWT_EXPIRATION_HOURS")
    
    ENCRYPTION_KEY: str = Field(default="your-encryption-key-change-this", env="ENCRYPTION_KEY")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=3600, env="RATE_LIMIT_WINDOW")
    
    # Monitoring and Analytics
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    METRICS_PORT: int = Field(default=9090, env="METRICS_PORT")
    
    APM_ENABLED: bool = Field(default=False, env="APM_ENABLED")
    APM_SERVICE_NAME: str = Field(default="ascend", env="APM_SERVICE_NAME")
    APM_SERVER_URL: str = Field(default="http://localhost:8200", env="APM_SERVER_URL")
    
    # Development Configuration
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="production", env="ENVIRONMENT")
    
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000"],
        env="ALLOWED_ORIGINS"
    )
    
    # Feature Flags
    ENABLE_ADVANCED_ANALYTICS: bool = Field(default=True, env="ENABLE_ADVANCED_ANALYTICS")
    ENABLE_PEER_LEARNING: bool = Field(default=False, env="ENABLE_PEER_LEARNING")
    ENABLE_VIRTUAL_TUTORING: bool = Field(default=False, env="ENABLE_VIRTUAL_TUTORING")
    ENABLE_CAREER_GUIDANCE: bool = Field(default=False, env="ENABLE_CAREER_GUIDANCE")
    
    # Notification Configuration
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USERNAME: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    
    PUSH_NOTIFICATION_ENABLED: bool = Field(default=False, env="PUSH_NOTIFICATION_ENABLED")
    FIREBASE_CREDENTIALS_PATH: Optional[str] = Field(default=None, env="FIREBASE_CREDENTIALS_PATH")
    
    # Storage Configuration
    STORAGE_TYPE: str = Field(default="local", env="STORAGE_TYPE")
    STORAGE_PATH: str = Field(default="./storage", env="STORAGE_PATH")
    MAX_FILE_SIZE: str = Field(default="10MB", env="MAX_FILE_SIZE")
    
    # Cloud Storage (AWS S3)
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")
    AWS_S3_BUCKET: Optional[str] = Field(default=None, env="AWS_S3_BUCKET")
    
    # Backup Configuration
    BACKUP_ENABLED: bool = Field(default=True, env="BACKUP_ENABLED")
    BACKUP_SCHEDULE: str = Field(default="0 2 * * *", env="BACKUP_SCHEDULE")
    BACKUP_RETENTION_DAYS: int = Field(default=30, env="BACKUP_RETENTION_DAYS")
    BACKUP_PATH: str = Field(default="./backups", env="BACKUP_PATH")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        validate_assignment = True
        extra = "ignore"
    
    def model_post_init(self, __context):
        """Post-initialization processing."""
        # Parse ALLOWED_ORIGINS if it's a string
        try:
            if isinstance(self.ALLOWED_ORIGINS, str):
                self.ALLOWED_ORIGINS = [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
        except Exception:
            # Fallback to default if parsing fails
            self.ALLOWED_ORIGINS = ["http://localhost:3000"]
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.ENVIRONMENT.lower() == "development" or self.DEBUG
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENVIRONMENT.lower() == "production" and not self.DEBUG
    
    @property
    def has_gemini_config(self) -> bool:
        """Check if Gemini is configured."""
        return bool(self.GOOGLE_API_KEY and self.GOOGLE_API_KEY != "your_google_api_key_here")
    
    @property
    def has_calendar_integration(self) -> bool:
        """Check if calendar integration is configured."""
        return bool(self.GOOGLE_CALENDAR_API_KEY and self.GOOGLE_CALENDAR_ID)
    
    @property
    def has_lms_integration(self) -> bool:
        """Check if any LMS integration is configured."""
        return any([
            self.CANVAS_API_KEY and self.CANVAS_BASE_URL,
            self.BLACKBOARD_API_KEY and self.BLACKBOARD_BASE_URL,
            self.MOODLE_API_KEY and self.MOODLE_BASE_URL
        ])
    
    @property
    def has_email_config(self) -> bool:
        """Check if email configuration is available."""
        return all([
            self.SMTP_HOST,
            self.SMTP_USERNAME,
            self.SMTP_PASSWORD
        ])
    
    @property
    def has_cloud_storage(self) -> bool:
        """Check if cloud storage is configured."""
        return all([
            self.AWS_ACCESS_KEY_ID,
            self.AWS_SECRET_ACCESS_KEY,
            self.AWS_S3_BUCKET
        ])


# Global settings instance
settings = Settings()
