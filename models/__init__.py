"""
Database models for the Ascend system.
Note: This project now uses MongoDB instead of SQLAlchemy models.
All data is stored as documents in MongoDB collections.
"""

# MongoDB collections used:
# - users: User information and session data
# - queries: All user queries and responses
# - assessments: Learning assessment history
# - schedules: Schedule optimization history
# - materials: Learning material generation history
# - guidance: Guidance and advice history

__all__ = []
